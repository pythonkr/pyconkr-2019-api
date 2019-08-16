from datetime import datetime

from django.contrib import admin
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.utils.formats import localize
from django.utils.html import format_html_join, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from graphql_relay import from_global_id, to_global_id
from iamport import Iamport
from import_export import fields
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from api.models.profile import Profile
from ticket.models import Ticket, TicketProduct, TicketForRegistration, Registration
from ticket.schemas import create_iamport


# seoul_timezone = pytz.timezone('Asia/Seoul')


class TicketProductResource(resources.ModelResource):
    class Meta:
        model = TicketProduct


class TicketProductAdmin(ImportExportModelAdmin):
    resource_class = TicketProductResource
    list_display = ('active', 'type', 'name', 'total', 'remaining_count', 'owner_profile', 'price',
                    'is_editable_price', 'is_unique_in_type', 'active', 'cancelable_date',
                    'ticket_open_at', 'ticket_close_at')
    search_fields = ['type', 'ticket_close_at']
    list_filter = ('type', 'ticket_close_at',)
    autocomplete_fields = ['owner', 'ticket_for']

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
    # registrations = fields.Field()
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

    # def dehydrate_registrations(self, ticket):
    #     return '\n'.join([localize(timezone.localtime(r.registered_at))
    #                       for r in ticket.registration_set.all()])


class TicketAdmin(ImportExportModelAdmin):
    resource_class = TicketResource
    autocomplete_fields = ['owner']
    list_display = ('id', 'status', 'product_type', 'product', 'registrations', 'owner_oauth_type', 'owner_name',
                    'owner_email', 'owner_organization', 'is_domestic_card', 'merchant_uid', 'amount', 'imp_uid',
                    'paid_at', 'options_str', 'cancelled_at', 'reason')
    search_fields = ['id', 'owner__profile__email', 'owner__profile__name_ko', 'owner__profile__name_en',
                     'merchant_uid', 'imp_uid', 'reason']
    list_filter = (
        ('is_domestic_card', admin.BooleanFieldListFilter),
        'status',
        'product__type',
        ('product', admin.RelatedOnlyFieldListFilter),
    )
    actions = ['refund', 'set_paid', 'register']

    def options_str(self, obj):
        if not obj.options:
            return ''
        if isinstance(obj.options, str):
            return obj.options
        return '\n'.join([f'{k}: {v}' for k, v in obj.options.items()])

    def register(self, request, queryset):
        for ticket in queryset:
            ticket.registration_set.create(registered_at=timezone.now())

    def registrations(self, obj):
        return format_html_join(
            mark_safe('<br>'), '{}',
            ((localize(timezone.localtime(r.registered_at)),)
             for r in obj.registration_set.all()))

    def refund(self, request, queryset):
        for ticket in queryset:
            if ticket.status != Ticket.STATUS_PAID:
                self.message_user(request, message=_('이미 환불된 티켓이거나 결제되지 않은 티켓입니다.'), level=messages.ERROR)
                return
            if ticket.amount == 0:
                ticket.status = Ticket.STATUS_CANCELLED
                ticket.reason = '무료 티켓 취소'
                ticket.cancelled_at = timezone.now()
                ticket.save()
                continue

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


class TicketForRegistrationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['owner']
    list_display = ('owner_name_with_reg', 'id', 'owner_email', 'product_type', 'status', 'registrations', 'product',)
    search_fields = ['id', 'owner__profile__email', 'owner__profile__name_ko', 'owner__profile__name_en']
    list_filter = ('status', 'product__type',)
    actions = ['register']

    def owner_name_with_reg(self, obj):
        global_id = to_global_id('TicketNode', obj.id)
        url = reverse('ticket_issue', args=[global_id])
        return format_html(f'<a class="button" href="{url}" target="_blank">{obj.owner_name}</a>')

    owner_name_with_reg.short_description = '이름'

    def registrations(self, obj):
        return format_html_join(
            mark_safe('<br>'), '{}',
            ((localize(timezone.localtime(r.registered_at)),) for r in obj.registration_set.all()))

    def options_str(self, obj):
        if not obj.options:
            return ''
        if isinstance(obj.options, str):
            return obj.options
        return '\n'.join([f'{k}: {v}' for k, v in obj.options.items()])

    def get_search_results(self, request, queryset, search_term):
        # INFO: 모든 유져의 리스트를 조회할 수 없도록 한다.
        if not search_term:
            return TicketForRegistration.objects.none(), False

        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # INFO: QR 코드로 읽는 경우를 가정한다.
        if search_term.startswith('https://www.pycon.kr/ticket/my-ticket?id='):
            global_id = search_term.replace('https://www.pycon.kr/ticket/my-ticket?id=', '')
            _, pk = from_global_id(global_id)
            queryset = Ticket.objects.filter(id=pk)
            return queryset, False

        return queryset, use_distinct


admin.site.register(TicketForRegistration, TicketForRegistrationAdmin)


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('owner_name', 'owner_email', 'registered_at')
    list_filter = ('ticket__product__type',)
    search_fields = ('ticket__owner__profile__email',
                     'ticket__owner__profile__name_ko', 'ticket__owner__profile__name_en',)


admin.site.register(Registration, RegistrationAdmin)
