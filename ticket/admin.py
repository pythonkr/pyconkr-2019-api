import datetime

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from graphql_extensions.exceptions import GraphQLError
from iamport import Iamport

from django.contrib import messages

from api.models.profile import Profile
from ticket.models import Ticket, TicketProduct
from ticket.schemas import create_iamport


class TicketProductAdmin(admin.ModelAdmin):
    list_display = ('active', 'type', 'name', 'desc', 'total', 'owner_profile', 'price',
                    'is_editable_price', 'is_unique_in_type', 'active', 'cancelable_date',
                    'ticket_open_at', 'ticket_close_at', 'warning')

    def owner_profile(self, obj):
        if obj.owner:
            profile, _ = Profile.objects.get_or_create(user=obj.owner)
            return profile
        return ''


admin.site.register(TicketProduct, TicketProductAdmin)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'owner_profile', 'product', 'is_domestic_card', 'merchant_uid', 'amount',
                    'status', 'imp_uid', 'paid_at', 'options_str', 'cancelled_at')
    search_fields = ['owner__profile__email', 'owner__profile__name_ko', 'owner__profile__name_en',
                     'merchant_uid', 'imp_uid']
    list_filter = (
        ('product', admin.RelatedOnlyFieldListFilter),
        ('is_domestic_card', admin.BooleanFieldListFilter),
        'status',
    )
    actions = ['refund']

    def owner_profile(self, obj):
        if obj.owner:
            profile, _ = Profile.objects.get_or_create(user=obj.owner)
            return profile
        return ''

    def options_str(self, obj):
        if not obj.options:
            return ''
        if isinstance(obj.options, str):
            return obj.options
        return '\n'.join([f'{k}: {v}' for k, v in obj.options.items()])

    def refund(self, request, queryset):
        for ticket in queryset:
            if ticket.status != Ticket.STATUS_PAID:
                raise GraphQLError(_('이미 환불된 티켓이거나 결제되지 않은 티켓입니다.'))
            try:
                iamport = create_iamport(ticket.is_domestic_card)
                response = iamport.cancel(u'티켓 환불', imp_uid=ticket.imp_uid)
            except Iamport.ResponseError as e:
                self.message_user(request, message=e.message, level=messages.ERROR)
                return
            except Iamport.HttpError as e:
                self.message_user(request, message=e._('환불이 실패했습니다'), level=messages.ERROR)
                return
            ticket.status = Ticket.STATUS_CANCELLED
            ticket.cancelled_at = datetime.fromtimestamp(response['cancelled_at'])
            ticket.cancel_receipt_url = response['cancel_receipt_urls'][0]
            ticket.save()


admin.site.register(Ticket, TicketAdmin)
