from datetime import datetime
import graphene
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.exceptions import GraphQLError

from iamporter import Iamporter
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from api.models.schedule import Schedule
from api.models.ticket import EarlyBirdTicket, TicketSetting


class EarlyBirdTicketNode(DjangoObjectType):
    class Meta:
        model = EarlyBirdTicket
        description = """
        EarlyBirdTicket
        """


class PaymentInput(graphene.InputObjectType):
    card_number = graphene.String()
    expiry = graphene.String()
    birth = graphene.String()
    pwd_2digit = graphene.String()


class BuyEarlyBirdTicket(graphene.Mutation):
    ticket = graphene.Field(EarlyBirdTicketNode)

    class Arguments:
        payment = PaymentInput(required=True)

    @login_required
    def mutate(self, info, payment):
        permitted_settings = settings.PERMITTED_SETTINGS
        if not permitted_settings:
            raise GraphQLError(f'{settings.PERMITTED_SETTINGS_PATH}가 설정되어 있지 않습니다.')
        client = Iamporter(imp_key=permitted_settings['IMP_KEY'],
                           imp_secret=permitted_settings['IMP_SECRET'])
        schedule = Schedule.objects.last()
        ticket_setting = TicketSetting.objects.last()
        remain_ticket_cnt = ticket_setting.early_bird_ticket_cnt - \
                            EarlyBirdTicket.objects.filter(
                                paid_at__isnull=False, is_refund=False).count()
        if remain_ticket_cnt <= 0:
            raise GraphQLError(_('얼리버드 티켓이 모두 판매되었습니다.'))
        if not schedule.earlybird_ticket_start_at or \
                schedule.earlybird_ticket_start_at > timezone.now():
            raise GraphQLError(_('얼리버드 티켓 판매가 아직 시작되지 않았습니다.'))
        if schedule.earlybird_ticket_finish_at and \
                schedule.earlybird_ticket_finish_at < timezone.now():
            raise GraphQLError(_('얼리버드 티켓 판매가 종료되었습니다.'))
        merchant_uid = f'merchant_{timezone.now().timestamp()}'
        amount = ticket_setting.early_bird_ticket_price
        name = "PyConKorea_EarlyBirdTicket"
        response = client.create_payment(
            merchant_uid=merchant_uid,
            name=name,
            amount=amount,
            **payment
        )
        if amount != response['amount']:
            pass
        if name != response['name']:
            pass
        if response['status'] != 'paid':
            raise GraphQLError(_('결제가 실패했습니다.'))

        ticket = EarlyBirdTicket.objects.create(
            owner=info.context.user,
            imp_uid=response['imp_uid'],
            pg_tid=response['pg_tid'],
            receipt_url=response['receipt_url'],
            paid_at=datetime.fromtimestamp(response['paid_at'])
        )

        return BuyEarlyBirdTicket(ticket=ticket)


class Mutations(graphene.ObjectType):
    buy_early_bird_ticket = BuyEarlyBirdTicket.Field()


class Query(graphene.ObjectType):
    pass
