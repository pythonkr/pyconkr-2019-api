from modeltranslation.translator import register, TranslationOptions

from ticket.models import TicketProduct, OptionDesc


@register(TicketProduct)
class TicketProductTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)


@register(OptionDesc)
class OptionDescTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)
