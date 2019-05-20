from modeltranslation.translator import register, TranslationOptions

from ticket.models import TicketProduct


@register(TicketProduct)
class TicketProductTranslationOptions(TranslationOptions):
    fields = ('name', 'desc', 'warning',)
