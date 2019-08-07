from datetime import datetime

import graphene
from constance import config
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.exceptions import GraphQLError, PermissionDenied
from graphql_relay import from_global_id
from iamport import Iamport

from api.schemas.common import has_staff_permission, SeoulDateTime, has_owner_permission
from ticket.models import TicketProduct, Ticket


class TicketTypeNode(graphene.Enum):
    CONFERENCE = TicketProduct.TYPE_CONFERENCE
    GROUP_CONFERENCE = TicketProduct.TYPE_GROUP_CONFERENCE
    YOUNG_CODER = TicketProduct.TYPE_YOUNG_CODER
    CHILD_CARE = TicketProduct.TYPE_CHILD_CARE
    TUTORIAL = TicketProduct.TYPE_TUTORIAL
    SPRINT = TicketProduct.TYPE_SPRINT
    HEALTH_CARE = TicketProduct.TYPE_HEALTH_CARE


class TicketProductNode(DjangoObjectType):
    class Meta:
        model = TicketProduct
        exclude_fields = ['ticket_set']

    type = TicketTypeNode()
    purchase_count = graphene.Int(description='로그인 했을 때에는 이 값에 구매한 티켓 개수가 들어갑니다.')
    is_sold_out = graphene.Boolean(description='True면 매진, False면 판매중 입니다.')
    remaining_count = graphene.Int(description='해당 제품에 남아있는 티켓 개수입니다.')
    is_purchased = graphene.Boolean(description='True면 유저가 해당 티켓을 구매하였으면 True가 반환됩니다. '
                                                '컨퍼런스와 같이 티켓이 여러 종류로 판매되는 경우 하나라도 구매했으면 True가 반환됩니다.')
    available = graphene.Boolean(description='True면 유저가 티켓을 구매할 수 있습니다. '
                                             '컨퍼런스와 같이 티켓이 여러 종류로 판매되는 경우 하나라도 구매했으면 False가 반환됩니다.'
                                             '아이돌봄이나 영코더는 참가자 1인당 하루 2매까지만 구매가 가능합니다')

    def resolve_purchase_count(self, info):
        if info.context.user.is_authenticated:
            return self.ticket_set.filter(owner=info.context.user).count()
        return 0

    def resolve_is_sold_out(self, info):
        return self.is_sold_out

    def resolve_remaining_count(self, info):
        return self.remaining_count

    def resolve_is_purchased(self, info):
        user = info.context.user
        if not user.is_authenticated:
            return False
        if self.is_unique_in_type:
            return Ticket.objects.filter(
                owner=user, product__type=self.type, status=Ticket.STATUS_PAID
            ).exists()
        return Ticket.objects.filter(
            owner=user, product__id=self.id, status=Ticket.STATUS_PAID
        ).exists()

    def resolve_available(self, info):
        return self.is_available(info.context.user)


class TicketNode(DjangoObjectType):
    class Meta:
        model = Ticket
        interfaces = (graphene.relay.Node,)
        description = """
        Ticket
        """

    registered_at = graphene.Field(SeoulDateTime)
    ticket_id = graphene.Int(source='ticket_id')


class PaymentInput(graphene.InputObjectType):
    is_domestic_card = graphene.Boolean(default_value=True)
    amount = graphene.Int(
        default_value=0,
        description='결제할 금액을 의미합니다. 수정 가능한 상품인 경우(개인후원)에만 사용됩니다.'
    )
    card_number = graphene.String(description='결제에 사용할 카드 번호입니다. (e.g, xxxx-xxxx-xxxx-xxxx)')
    expiry = graphene.String(description='결제에 사용하는 카드의 만료 기간입니다. (e.g, YYYY-MM)')
    birth = graphene.String(
        description='한국 카드일 때 사용하며 생년월일의 형태를 가집니다.(e.g, 880101)')
    pwd_2digit = graphene.String(
        description='한국 카드일 때 사용하며 비밀번호 앞 2자리입니다.(e.g, 11)')
    buyer_email = graphene.String(
        description='구매자 이메일 주소입니다. 필수 옵션은 아닙니다.(e.g, pycon@pycon.kr)'
    )
    buyer_name = graphene.String(
        description='구매자 이름입니다. 필수 옵션은 아닙니다.(e.g, 홍길동)'
    )
    buyer_tel = graphene.String(
        description='구매자 전화 번호입니다. 필수 옵션은 아닙니다.(e.g, 02-1234-1234)'
    )


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
        user = info.context.user

        try:
            product = TicketProduct.objects.get(pk=product_id)
        except TicketProduct.DoesNotExist:
            raise GraphQLError(f'Ticket project is not exists.(product_id: {product_id})')
        if Ticket.objects.filter(owner=user, product=product, status=Ticket.STATUS_READY).exists():
            raise GraphQLError(_('결제가 진행 중입니다. 잠시 후 다시 시도해주세요. 문제가 지속 발생할 경우 support@pycon.kr로 연락주세요.'))
        if not product.is_available(info.context.user):
            raise GraphQLError(_('선택한 티켓은 구매할 수 없습니다.'))
        if product.is_minor_target_program() and not BuyTicket.has_conference_ticket(user):
            raise GraphQLError(_('영코더/아이돌봄 티켓은 컨퍼런스 티켓 구매자에게만 판매됩니다.'))
        if product.ticket_for.exists() and info.context.user not in product.ticket_for.all():
            raise GraphQLError(_('사용자에게 판매하는 티켓이 아닙니다.'))
        BuyTicket.check_product(product)
        if product.is_editable_price and product.price > payment.amount:
            raise GraphQLError(_(f'이 상품은 티켓 가격({payment.amount}원)보다 높은 가격으로 구매해야 합니다.'))
        try:
            ticket = Ticket.objects.create(
                is_domestic_card=payment.is_domestic_card,
                owner=user,
                product=product,
                amount=payment.amount,
                status=Ticket.STATUS_READY,
                options=options
            )

            if product.is_deposit_ticket:
                ticket.status = Ticket.STATUS_DEPOSIT_WAITING
                ticket.save()
                return BuyTicket(ticket=ticket)

            if product.price == 0:
                ticket.status = Ticket.STATUS_PAID
                ticket.save()
                return BuyTicket(ticket=ticket)
            try:
                payment_params = BuyTicket.get_payment_params(user, payment)
                response = BuyTicket.create_payment(product, payment, payment_params)
            except Iamport.ResponseError as e:
                raise GraphQLError(e.message)
            except Iamport.HttpError as e:
                raise GraphQLError(_(f'아이엠포트 결제가 실패하였습니다.({e.code})'))

            ticket.merchant_uid = response['merchant_uid']
            ticket.imp_uid = response['imp_uid']
            ticket.pg_tid = response['pg_tid']
            ticket.receipt_url = response['receipt_url']
            ticket.paid_at = datetime.fromtimestamp(response['paid_at'])
            ticket.status = response['status']
            ticket.save()

            return BuyTicket(ticket=ticket)
        except GraphQLError as e:
            ticket.status = Ticket.STATUS_ERROR
            ticket.reason = str(e)[:250]
            ticket.save()
            raise e

    @classmethod
    def check_product(cls, product):
        if product.is_sold_out:
            raise GraphQLError(_('티켓이 모두 판매되었습니다.'))
        if product.is_not_open_yet():
            raise GraphQLError(_('티켓 판매가 아직 시작되지 않았습니다.'))
        if product.is_closed():
            raise GraphQLError(_('티켓 판매가 종료되었습니다.'))

    @classmethod
    def create_payment(cls, product, payment, payment_params):
        payload = {
            'merchant_uid': f'pyconkr_{timezone.now().timestamp()}',
            'name': product.name_ko,
            **payment_params
        }

        iamport = create_iamport(payment.is_domestic_card)
        if payment.is_domestic_card:
            return iamport.pay_onetime(**payload)
        return iamport.pay_foreign(**payload)

    @classmethod
    def get_payment_params(cls, user, payment):
        required_field = ['card_number', 'expiry']
        if payment.is_domestic_card:
            required_field = ['card_number', 'expiry', 'birth', 'pwd_2digit']
        for attr in required_field:
            if getattr(payment, attr, None):
                continue
            raise ValueError(f'Could not find "{attr}" in payment')
        params = {k: v for k, v in payment.items() if v}
        if not params.get('buyer_email'):
            params['buyer_email'] = user.profile.email
        if not params.get('buyer_tel'):
            params['buyer_tel'] = user.profile.phone
        if not params.get('buyer_name'):
            params['buyer_name'] = user.profile.name
        return params

    @classmethod
    def has_conference_ticket(cls, user):
        return Ticket.objects.filter(
            owner=user, status=Ticket.STATUS_PAID,
            product__type=TicketProduct.TYPE_CONFERENCE
        ).exists()


class CancelTicket(graphene.Mutation):
    ticket = graphene.Field(TicketNode)

    class Arguments:
        ticket_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, ticket_id):
        ticket_pk = from_global_id(ticket_id)[1]
        ticket = Ticket.objects.get(pk=ticket_pk)
        if ticket.owner != info.context.user:
            raise GraphQLError(_('다른 유저의 티켓을 환불할 수 없습니다.'))
        if ticket.status != Ticket.STATUS_PAID:
            raise GraphQLError(_('이미 환불된 티켓이거나 결제되지 않은 티켓입니다.'))
        if not ticket.product.is_cancelable_date():
            raise GraphQLError(_('환불 가능 기한이 지났습니다.'))
        if ticket.amount == 0:
            ticket.status = Ticket.STATUS_CANCELLED
            ticket.reason = '무료 티켓 취소'
            ticket.cancelled_at = timezone.now()
            ticket.save()
            return CancelTicket(ticket=ticket)
        try:
            iamport = create_iamport(ticket.is_domestic_card)
            response = iamport.cancel(u'티켓 환불', imp_uid=ticket.imp_uid)
        except Iamport.ResponseError as e:
            raise GraphQLError(e.message)
        except Iamport.HttpError as e:
            raise GraphQLError(_('환불이 실패했습니다'))

        if Ticket.STATUS_CANCELLED != response['status']:
            raise GraphQLError(_('환불이 실패했습니다'))
        ticket.status = Ticket.STATUS_CANCELLED
        ticket.cancelled_at = datetime.fromtimestamp(response['cancelled_at'])
        ticket.cancel_receipt_url = response['cancel_receipt_urls'][0]
        ticket.save()
        return CancelTicket(ticket=ticket)


def create_iamport(is_domestic_card):
    if is_domestic_card:
        return Iamport(imp_key=config.IMP_DOM_API_KEY,
                       imp_secret=config.IMP_DOM_API_SECRET)
    return Iamport(imp_key=config.IMP_INTL_API_KEY,
                   imp_secret=config.IMP_INTL_API_SECRET)


class RegisterTicket(graphene.Mutation):
    ticket = graphene.Field(TicketNode)

    class Arguments:
        ticket_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, ticket_id):
        user = info.context.user
        if not has_staff_permission(user):
            raise GraphQLError(_('스태프만 티켓을 등록할 수 있습니다.'))
        ticket_pk = from_global_id(ticket_id)[1]
        ticket = Ticket.objects.get(pk=ticket_pk)
        ticket.registered_at = timezone.now()
        ticket.save()
        return RegisterTicket(ticket=ticket)


class Mutations(graphene.ObjectType):
    buy_ticket = BuyTicket.Field()
    cancel_ticket = CancelTicket.Field()


def get_ticket_product(product_type, user):
    return TicketProduct.objects.filter(type=product_type, active=True) \
        .filter(Q(ticket_for=user) | Q(ticket_for__isnull=True))


class Query(graphene.ObjectType):
    ticket_product = graphene.Field(TicketProductNode)
    conference_products = graphene.List(TicketProductNode)
    young_coder_products = graphene.List(TicketProductNode)
    child_care_products = graphene.List(TicketProductNode)
    tutorial_products = graphene.List(TicketProductNode)
    sprint_products = graphene.List(TicketProductNode)
    health_care_products = graphene.List(TicketProductNode)

    my_tickets = graphene.List(TicketNode)
    ticket = graphene.Field(
        TicketNode,
        global_id=graphene.ID(),
        id=graphene.Int())

    my_ticket = graphene.Field(
        TicketNode,
        id=graphene.ID())

    def resolve_ticket(self, info, global_id=None, id=None):
        ticket = None
        if global_id:
            ticket = Ticket.objects.get(pk=from_global_id(global_id)[1])
        if id:
            ticket = Ticket.objects.get(pk=id)

        if not ticket:
            return None
        if not has_owner_permission(info.context.user, ticket.owner):
            raise PermissionDenied()
        return ticket

    def resolve_my_ticket(self, info, id=None):
        ticket = Ticket.objects.get(pk=from_global_id(id)[1])
        if not has_owner_permission(info.context.user, ticket.owner):
            raise PermissionDenied()
        return ticket

    def resolve_conference_products(self, info):
        conference_product = get_ticket_product(TicketProduct.TYPE_CONFERENCE, info.context.user)
        group_conference_product = get_ticket_product(TicketProduct.TYPE_GROUP_CONFERENCE, info.context.user)
        return conference_product | group_conference_product

    def resolve_young_coder_products(self, info):
        return get_ticket_product(TicketProduct.TYPE_YOUNG_CODER, info.context.user)

    def resolve_child_care_products(self, info):
        return get_ticket_product(TicketProduct.TYPE_CHILD_CARE, info.context.user)

    def resolve_tutorial_products(self, info):
        return get_ticket_product(TicketProduct.TYPE_TUTORIAL, info.context.user)

    def resolve_sprint_products(self, info):
        return get_ticket_product(TicketProduct.TYPE_SPRINT, info.context.user)

    def resolve_health_care_products(self, info):
        return get_ticket_product(TicketProduct.TYPE_HEALTH_CARE, info.context.user)

    @login_required
    def resolve_my_tickets(self, info):
        return Ticket.objects.filter(owner=info.context.user) \
            .filter((Q(status=Ticket.STATUS_PAID) | Q(status=Ticket.STATUS_CANCELLED)))
