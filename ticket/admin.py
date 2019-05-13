from django.contrib import admin

from api.models.profile import Profile
from ticket.models import Ticket, TicketProduct, OptionDesc


class OptionDescAdmin(admin.TabularInline):
    model = OptionDesc


class TicketProductAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'desc', 'total', 'owner_profile', 'price',
                    'is_editable_price', 'is_unique_in_type', 'active', 'cancelable_date',
                    'ticket_open_at', 'ticket_close_at')
    inlines = [OptionDescAdmin]

    def owner_profile(self, obj):
        if obj.owner:
            profile, _ = Profile.objects.get_or_create(user=obj.owner)
            return profile
        return ''


admin.site.register(TicketProduct, TicketProductAdmin)
admin.site.register(OptionDesc)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('owner_profile', 'product', 'is_foreign', 'merchant_uid', 'amount',
                    'status', 'imp_uid', 'paid_at', 'options_str')

    def owner_profile(self, obj):
        if obj.owner:
            profile, _ = Profile.objects.get_or_create(user=obj.owner)
            return profile
        return ''

    def options_str(self, obj):
        if not obj.options:
            return ''
        return '\n'.join([f'{k}: {v}' for k, v in obj.options.items()])


admin.site.register(Ticket, TicketAdmin)
