from modeltranslation.translator import register, TranslationOptions

from notice.models import Notice


@register(Notice)
class NoticeTranslationOptions(TranslationOptions):
    fields = ('title',)
