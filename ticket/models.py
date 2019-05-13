from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

UserModel = get_user_model()


class TicketProduct(models.Model):
    TYPE_CONFERENCE = 'C'
    TYPE_YOUNG_CODER = 'Y'
    TYPE_BABY_CARE = 'B'
    TYPE_TUTORIAL = 'T'
    TYPE_SPRINT = 'S'
    TYPE_HEALTH_CARE = 'H'

    type = models.CharField(max_length=1,
                            choices=(
                                (TYPE_CONFERENCE, _('컨퍼런스')),
                                (TYPE_YOUNG_CODER, _('영코더')),
                                (TYPE_BABY_CARE, _('아이돌봄')),
                                (TYPE_TUTORIAL, _('튜토리얼')),
                                (TYPE_SPRINT, _('스프린트')),
                                (TYPE_HEALTH_CARE, _('체육시간')),
                            ), default=TYPE_CONFERENCE)
    name = models.CharField(max_length=255, null=True)
    desc = models.TextField(blank=True, default='')
    start_at = models.DateTimeField(null=True, blank=True,
                                    help_text='행사가 시작되는 일시입니다.')
    finish_at = models.DateTimeField(null=True, blank=True,
                                     help_text='행사가 종료되는 일시입니다.')
    total = models.IntegerField(default=0,
                                help_text='판매할 티켓의 총 개수입니다.')
    owner = models.ForeignKey(UserModel, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.IntegerField(default=0)
    is_editable_price = models.BooleanField(default=False,
                                            help_text='개인후원과 같이 가격을 상향조정할 수 있는지 여부를 나타냅니다.')
    is_unique_in_type = models.BooleanField(default=True,
                                            help_text='같은 타입간에 하나만 구매가 가능한지 여부를 나타냅니다. '
                                                      '대표적으로 컨퍼런스티켓이 이에 해당합니다.')
    active = models.BooleanField(default=True,
                                 help_text='해당 티켓 판매가 활성화되었는지를 저장합니다. True이면 사용자에게 노출됩니다.')
    cancelable_date = models.DateTimeField(null=True, blank=True,
                                           help_text='결재 취소가 가능한 기한입니다. 이 일시 이후에는 취소가 불가합니다.')
    ticket_open_at = models.DateTimeField(null=True, blank=True,
                                          help_text='티켓 판매 시작 일시입니다.')
    ticket_close_at = models.DateTimeField(null=True, blank=True,
                                           help_text='티켓 판매 종료 일시입니다.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_cancelable(self):
        return not self.cancelable_date

    @property
    def remaining_count(self):
        return self.total - self.ticket_set.filter(status=TransactionMixin.STATUS_PAID).count()

    def is_sold_out(self):
        return self.remaining_count <= 0

    def is_not_open_yet(self):
        return not self.ticket_open_at or self.ticket_open_at > timezone.now()

    def is_closed(self):
        return self.ticket_close_at and self.ticket_close_at < timezone.now()

    def __str__(self):
        return self.name


class OptionDesc(models.Model):
    TYPE_BOOL = 'B'
    TYPE_NUMBER = 'N'
    TYPE_STRING = 'S'

    type = models.CharField(max_length=1,
                            choices=(
                                (TYPE_BOOL, 'BOOL'),
                                (TYPE_NUMBER, 'NUMBER'),
                                (TYPE_STRING, 'STRING')
                            ), default=TYPE_STRING)
    key = models.CharField(max_length=100, null=True, help_text='ticket에 저장되는 데이터의 KEY값입니다.')
    name = models.CharField(max_length=255, blank=True, default='', help_text='ticket 판매시 노출되는 이름입니다')
    desc = models.TextField(blank=True, default='', help_text='ticket 판매시 노출되는 설명입니다')
    product = models.ForeignKey(TicketProduct, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TransactionMixin(models.Model):
    STATUS_READY = 'ready'
    STATUS_PAID = 'paid'
    STATUS_DELETE = 'delete'
    STATUS_CANCELLED = 'cancelled'

    is_foreign = models.BooleanField(default=False)
    amount = models.IntegerField(
        default=0,
        help_text='아이엠포트를 통해 결재한 가격입니다.'
    )
    merchant_uid = models.CharField(max_length=100, blank=True, default='',
                                    help_text='파이콘 한국에서 발행하는 주문번호입니다. 영수증에 출력됩니다.')
    imp_uid = models.CharField(max_length=255, null=True, blank=True,
                               help_text='아이엠포트 uid입니다. 이 값은 환불 시에 사용됩니다.')
    pg_tid = models.CharField(max_length=127, null=True, blank=True,
                              help_text='PG사 Transaction ID입니다.')
    receipt_url = models.CharField(max_length=255, null=True, blank=True,
                                   help_text='영수증 URL입니다. 이 값은 카드 결제 내역을 보여줄 때에 사용됩니다.')
    paid_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=10,
                              choices=(
                                  (STATUS_READY, 'Ready'),
                                  (STATUS_PAID, 'Paid'),
                                  (STATUS_DELETE, 'Deleted'),
                                  (STATUS_CANCELLED, 'Cancelled')
                              ), default=STATUS_READY)

    class Meta:
        abstract = True


class Ticket(TransactionMixin, models.Model):
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    product = models.ForeignKey(TicketProduct, on_delete=models.CASCADE)
    options = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def ticket_id(self):
        # TODO: 내년엔 year를 실제 데이터로 사용하도록 바꿔주셔야 합니다 ;)
        year = 2019
        return f'{year}{self.id.vfill(8)}'
