from datetime import datetime

import graphene
from constance import config
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.exceptions import GraphQLError
from iamporter import Iamporter

from ticket.models import TransactionMixin, TicketProduct, Ticket, OptionDesc


class TicketTypeNode(graphene.Enum):
    CONFERENCE = TicketProduct.TYPE_CONFERENCE
    YOUNG_CODER = TicketProduct.TYPE_YOUNG_CODER
    BABY_CARE = TicketProduct.TYPE_BABY_CARE
    TUTORIAL = TicketProduct.TYPE_TUTORIAL
    SPRINT = TicketProduct.TYPE_SPRINT
    HEALTH_CARE = TicketProduct.TYPE_HEALTH_CARE

class OptionDescTypeNode(graphene.Enum):
    BOOL = OptionDesc.TYPE_BOOL
    NUMBER = OptionDesc.TYPE_NUMBER
    STRING = OptionDesc.TYPE_STRING

class OptionDescNode(DjangoObjectType):
    class Meta:
        model = OptionDesc

    type = OptionDescTypeNode()

class TicketProductNode(DjangoObjectType):
    class Meta:
        model = TicketProduct
        exclude_fields = ['ticket_set']
        interfaces = (graphene.relay.Node,)

    type = TicketTypeNode()
    purchase_count = graphene.Int(description='로그인 했을 때에는 이 값에 구매한 티켓 개수가 들어갑니다.')

    def resolve_purchase_count(self, info):
        if info.context.user.is_authenticated:
            return self.ticket_set.filter(owner=info.context.user).count()
        return 0



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
    birth = graphene.String(
        description='한국 카드일 때 사용하며 생년월일의 형태를 가집니다.(e.g., 880101)')
    pwd_2digit = graphene.String(
        description='한국 카드일 때 사용하며 비밀번호 앞 2자리입니다.(e.g., 11)')


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
        payment_params = BuyTicket.get_payment_params(payment)
        client = BuyTicket.create_iamport_client(payment)
        try:
            product = TicketProduct.objects.get(pk=product_id)
        except TicketProduct.DoesNotExist:
            raise GraphQLError(f'Ticket project is not exists.(product_id: {product_id})')
        BuyTicket.check_schedule(product)
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

    @classmethod
    def check_schedule(cls, product):
        if product.is_sold_out():
            raise GraphQLError(_('티켓이 모두 판매되었습니다.'))
        if product.is_not_open_yet():
            raise GraphQLError(_('티켓 판매가 아직 시작되지 않았습니다.'))
        if product.is_closed():
            raise GraphQLError(_('티켓 판매가 종료되었습니다.'))

    @classmethod
    def create_iamport_client(cls, payment):
        if payment.is_domestic_card:
            client = Iamporter(imp_key=config.IMP_DOM_API_KEY,
                               imp_secret=config.IMP_DOM_API_SECRET)
        else:
            client = Iamporter(imp_key=config.IMP_INTL_API_KEY,
                               imp_secret=config.IMP_INTL_API_SECRET)
        return client

    @classmethod
    def get_payment_params(cls, payment):
        required_field = ['card_number', 'expiry']
        if payment.is_domestic_card:
            required_field = ['card_number', 'expiry', 'birth', 'pwd_2digit']
        for attr in required_field:
            if getattr(payment, attr, None):
                continue
            raise ValueError(f'Could not find "{attr}" in payment')
        return {k: v for k, v in payment.items() if k in required_field}


class Mutations(graphene.ObjectType):
    buy_ticket = BuyTicket.Field()


class Query(graphene.ObjectType):
    ticket_product = graphene.relay.Node.Field(TicketProductNode)
    conference_products = graphene.List(TicketProductNode)
    young_coder_products = graphene.List(TicketProductNode)
    baby_care_products = graphene.List(TicketProductNode)
    tutorial_products = graphene.List(TicketProductNode)
    sprint_products = graphene.List(TicketProductNode)
    health_care_products = graphene.List(TicketProductNode)

    def resolve_conference_products(self, info):
        return TicketProduct.objects.filter(type=TicketProduct.TYPE_CONFERENCE)

    def resolve_young_coder_products(self, info):
        return TicketProduct.objects.filter(type=TicketProduct.TYPE_YOUNG_CODER)

    def resolve_baby_care_products(self, info):
        return TicketProduct.objects.filter(type=TicketProduct.TYPE_BABY_CARE)

    def resolve_tutorial_products(self, info):
        return TicketProduct.objects.filter(type=TicketProduct.TYPE_TUTORIAL)

    def resolve_sprint_products(self, info):
        return TicketProduct.objects.filter(type=TicketProduct.TYPE_SPRINT)

    def resolve_health_care_products(self, info):
        return TicketProduct.objects.filter(type=TicketProduct.TYPE_HEALTH_CARE)
