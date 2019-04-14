from modeltranslation.translator import register, TranslationOptions

from api.models.schedule import Schedule
from api.models.sponsor import Sponsor, SponsorLevel
from api.models.profile import Profile
from api.models.program import Place, Category, Difficulty, Program, Presentation

@register(Schedule)
class ScheduleTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('name', 'bio',)


@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Difficulty)
class DifficultyTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Program)
class ProgramTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)


@register(Presentation)
class PresentationTranslationOptions(TranslationOptions):
    fields = ('background_desc',)


@register(SponsorLevel)
class SponsorLevelTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Sponsor)
class SponsorTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)
