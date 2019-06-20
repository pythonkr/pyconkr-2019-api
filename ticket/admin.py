from datetime import datetime

from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from iamport import Iamport
from import_export import fields
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from api.models.profile import Profile
from ticket.models import Ticket, TicketProduct
from ticket.schemas import create_iamport


class TicketProductAdmin(admin.ModelAdmin):
    list_display = ('active', 'type', 'name', 'desc', 'total', 'remaining_count', 'owner_profile', 'price',
                    'is_editable_price', 'is_unique_in_type', 'active', 'cancelable_date',
                    'ticket_open_at', 'ticket_close_at', 'warning')

    def owner_profile(self, obj):
        if obj.owner:
            profile, _ = Profile.objects.get_or_create(user=obj.owner)
            return profile
        return ''


admin.site.register(TicketProduct, TicketProductAdmin)


class TicketResource(resources.ModelResource):
    class Meta:
        model = Ticket

    id = fields.Field(column_name='id', attribute='id')
    name = fields.Field(column_name='name', attribute='owner__profile__name')
    email = fields.Field(column_name='email', attribute='owner__profile__email')
    product = fields.Field(column_name='product', attribute='product')
    status = fields.Field(column_name='status', attribute='status')
    is_domestic_card = fields.Field(column_name='is_domestic_card', attribute='is_domestic_card')
    amount = fields.Field(column_name='amount', attribute='amount')
    imp_uid = fields.Field(column_name='imp_uid', attribute='imp_uid')
    paid_at = fields.Field(column_name='paid_at', attribute='paid_at')
    cancelled_at = fields.Field(column_name='cancelled_at', attribute='cancelled_at')
    receipt_url = fields.Field(column_name='receipt_url', attribute='receipt_url')
    created_at = fields.Field(column_name='created_at', attribute='created_at')
    updated_at = fields.Field(column_name='created_at', attribute='updated_at')


class TicketAdmin(ImportExportModelAdmin):
    resource_class = TicketResource
    list_display = ('id', 'owner', 'owner_profile', 'product', 'is_domestic_card', 'merchant_uid', 'amount',
                    'status', 'imp_uid', 'paid_at', 'options_str', 'cancelled_at')
    search_fields = ['owner__profile__email', 'owner__profile__name_ko', 'owner__profile__name_en',
                     'merchant_uid', 'imp_uid']
    list_filter = (
        ('product', admin.RelatedOnlyFieldListFilter),
        ('is_domestic_card', admin.BooleanFieldListFilter),
        'status',
    )
    actions = ['refund', 'set_paid']

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
                self.message_user(request, message=_('이미 환불된 티켓이거나 결제되지 않은 티켓입니다.'), level=messages.ERROR)
                return
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
        self.message_user(request, message='환불이 성공했습니다.')

    def set_paid(self, request, queryset):
        queryset.update(status=Ticket.STATUS_PAID)


admin.site.register(Ticket, TicketAdmin)
