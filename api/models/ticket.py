from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

# pylint: disable=invalid-name
UserModel = get_user_model()


class TicketSetting(models.Model):
    early_bird_ticket_cnt = models.IntegerField(
        default=100,
        help_text='판매할 얼리버드 컨퍼런스 티켓의 개수입니다.'
    )
    early_bird_ticket_price = models.IntegerField(
        default=0,
        help_text='얼리버드 컨퍼런스 티켓 가격입니다.'
    )
    conference_ticket_cnt = models.IntegerField(
        default=100,
        help_text='판매할 일반 컨퍼런스 티켓의 개수입니다.'
    )
    conference_ticket_price = models.IntegerField(
        default=0,
        help_text='일반 컨퍼런스 티켓 가격입니다.'
    )


class TransactionMixin(models.Model):
    amount = models.IntegerField(
        default=0,
        help_text='아이엠포트를 통해 결재한 가격입니다.'
    )
    imp_uid = models.CharField(max_length=255, null=True, blank=True,
                               help_text='아이엠포트 uid입니다. 이 값은 환불 시에 사용됩니다.')
    pg_tid = models.CharField(max_length=127, null=True, blank=True,
                              help_text='PG사 Transaction ID입니다.')
    receipt_url = models.CharField(max_length=255, null=True, blank=True,
                                   help_text='영수증 URL입니다. 이 값은 카드 결제 내역을 보여줄 때에 사용됩니다.')
    paid_at = models.DateTimeField(null=True, blank=True)
    is_refund = models.BooleanField(default=False,
                                    help_text='환불되었는지를 구분하는 필드입니다')

    class Meta:
        abstract = True


class ConferenceTicket(TransactionMixin, models.Model):
    TYPE_EARLYBIRD = 'E'
    TYPE_REGULAR = 'R'
    TYPE_PATRON = 'P'
    type = models.CharField(max_length=1,
                            choices=(
                                (TYPE_REGULAR, _('일반')),
                                (TYPE_EARLYBIRD, _('얼리버드')),
                                (TYPE_PATRON, _('개인후원')),
                            ), default=TYPE_REGULAR)
    owner = models.OneToOneField(UserModel, null=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
