from modeltranslation.translator import register, TranslationOptions

from api.models import Sponsor, SponsorLevel
from api.models.profile import Profile
from api.models.program import \
    Conference, Place, Category, Difficulty, Program, Presentation

@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('name', 'bio',)

@register(Conference)
class ConferenceTranslationOptions(TranslationOptions):
    fields = ('name',)


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
    fields = ()

@register(SponsorLevel)
class SponsorLevelTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Sponsor)
class SponsorTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)
