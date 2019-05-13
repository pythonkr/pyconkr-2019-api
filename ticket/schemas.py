from datetime import datetime

import graphene
from constance import config
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.exceptions import GraphQLError
from iamporter import Iamporter

from ticket.models import TransactionMixin, TicketProduct, Ticket


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
    is_domestic_card = graphene.Boolean(required=True)
    card_number = graphene.String(required=True)
    expiry = graphene.String(required=True)
    birth = graphene.String()
    pwd_2digit = graphene.String()


class BuyTicket(graphene.Mutation):
    ticket = graphene.Field(TicketNode)

    class Arguments:
        product_id = graphene.ID(required=True)
        payment = PaymentInput(required=True)
        options = graphene.types.json.JSONString(default_value='{}')

    @login_required
    def mutate(self, info, product_id, payment, options):
        if not config.IMP_DOM_API_KEY or not config.IMP_INTL_API_KEY:
            raise GraphQLError(_('아이엠포트 계정 정보가 설정되어 있지 않습니다.'))
        payment_params = self.get_payment_params(payment)
        client = self.create_iamport_client(payment)
        try:
            product = TicketProduct.objects.get(pk=product_id)
        except TicketProduct.DoesNotExist:
            raise GraphQLError(f'Ticket project is not exists.(product_id: {product_id})')
        self.check_schedule(product)
        merchant_uid = f'merchant_{timezone.now().timestamp()}'
        amount = product.price
        name = product.name_ko
        response = client.create_payment(
            merchant_uid=merchant_uid,
            name=name,
            amount=amount,
            **payment_params
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

    def check_schedule(self, product):
        if product.is_sold_out():
            raise GraphQLError(_('티켓이 모두 판매되었습니다.'))
        if product.is_not_open_yet():
            raise GraphQLError(_('티켓 판매가 아직 시작되지 않았습니다.'))
        if product.is_closed():
            raise GraphQLError(_('티켓 판매가 종료되었습니다.'))

    def create_iamport_client(self, payment):
        if payment.is_domestic_card:
            client = Iamporter(imp_key=config.IMP_DOM_API_KEY,
                               imp_secret=config.IMP_DOM_API_SECRET)
        else:
            client = Iamporter(imp_key=config.IMP_INTL_API_KEY,
                               imp_secret=config.IMP_INTL_API_SECRET)
        return client

    def get_payment_params(self, payment):
        required_field = ['card_number', 'expiry']
        if payment.is_domestic_card:
            required_field = ['card_number', 'expiry', 'birth', 'pwd_2digit']
        for attr in required_field:
            if getattr(payment, attr, None):
                pass
            raise ValueError(f'Could not find "{attr}" in payment')
        return {k: v for k, v in payment.items() if k in required_field}


class Mutations(graphene.ObjectType):
    buy_ticket = BuyTicket.Field()


class Query(graphene.ObjectType):
    ticket_products = DjangoFilterConnectionField(TicketProductNode)
