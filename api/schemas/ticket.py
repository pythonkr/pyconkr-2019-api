from datetime import datetime

import graphene
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.exceptions import GraphQLError
from iamporter import Iamporter

from api.models.ticket import TransactionMixin, TicketProduct, Ticket


class TicketProductNode(DjangoObjectType):
    class Meta:
        model = TicketProduct
        filter_fields = ['type']
        interfaces = (graphene.relay.Node,)


class TicketNode(DjangoObjectType):
    class Meta:
        model = Ticket
        description = """
        Ticket
        """


class PaymentInput(graphene.InputObjectType):
    is_foreigner = graphene.Boolean()
    card_number = graphene.String()
    expiry = graphene.String()
    birth = graphene.String()
    pwd_2digit = graphene.String()


class BuyTicket(graphene.Mutation):
    ticket = graphene.Field(TicketNode)

    class Arguments:
        product_id = graphene.ID()
        payment = PaymentInput(required=True)
        options = graphene.types.json.JSONString(required=False)

    @login_required
    def mutate(self, info, product_id, payment, options):
        permitted_settings = settings.PERMITTED_SETTINGS
        if not permitted_settings:
            raise GraphQLError(f'{settings.PERMITTED_SETTINGS_PATH}가 설정되어 있지 않습니다.')
        client = Iamporter(imp_key=permitted_settings['IMP_KEY'],
                           imp_secret=permitted_settings['IMP_SECRET'])
        try:
            product = TicketProduct.objects.get(pk=product_id)
        except TicketProduct.DoesNotExist:
            raise GraphQLError(f'Ticket project is not exists.(product_id: {product_id})')

        if product.is_sold_out():
            raise GraphQLError(_('티켓이 모두 판매되었습니다.'))
        if product.is_not_open_yet():
            raise GraphQLError(_('티켓 판매가 아직 시작되지 않았습니다.'))
        if product.is_closed():
            raise GraphQLError(_('티켓 판매가 종료되었습니다.'))
        merchant_uid = f'merchant_{timezone.now().timestamp()}'
        amount = product.price
        name = product.name_ko
        response = client.create_payment(
            merchant_uid=merchant_uid,
            name=name,
            amount=amount,
            **payment
        )
        if response['status'] != TransactionMixin.STATUS_PAID:
            raise GraphQLError(_('결제가 실패했습니다.'))

        ticket = Ticket.objects.create(
            owner=info.context.user,
            product=product,
            amount=response['amount'],
            imp_uid=response['imp_uid'],
            pg_tid=response['pg_tid'],
            receipt_url=response['receipt_url'],
            paid_at=datetime.fromtimestamp(response['paid_at']),
            status=response['status'],
            options=options
        )

        return BuyTicket(ticket=ticket)


class Mutations(graphene.ObjectType):
    buy_ticket = BuyTicket.Field()


class Query(graphene.ObjectType):
    ticket_products = DjangoFilterConnectionField(TicketProductNode)