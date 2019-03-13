import graphene
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required

from django.db.models import Q
from api.models.program import Presentation
from api.models.program import Place, Category, Difficulty
from api.schemas.user import UserNode
from api.schemas.common import SeoulDateTime


class LanguageNode(graphene.Enum):
    KOREAN = Presentation.LANGUAGE_KOREAN
    ENGLISH = Presentation.LANGUAGE_ENGLISH


class DurationNode(graphene.Enum):
    SHORT = Presentation.DURATION_SHORT
    LONG = Presentation.DURATION_LONG


class PresentationNode(DjangoObjectType):
    class Meta:
        model = Presentation
        description = """
        Program which speakers present their presentations at Pycon Korea.
        It is one of the the most important program in Pycon Korea.
        """
    language = graphene.Field(LanguageNode)
    duration = graphene.Field(DurationNode)
    started_at = graphene.Field(SeoulDateTime)
    finished_at = graphene.Field(SeoulDateTime)


class PlaceNode(DjangoObjectType):
    class Meta:
        model = Place
        description = """
        It is the place where the program is held.
        This can be either in the room or in the lobby.
        """


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        description = """
        Category of presentation.
        """


class DifficultyNode(DjangoObjectType):
    class Meta:
        model = Difficulty
        description = """
        Difficulty of presentation.
        """


class PresentationInput(graphene.InputObjectType):
    name = graphene.String()
    name_ko = graphene.String()
    name_en = graphene.String()
    desc = graphene.String()
    desc_ko = graphene.String()
    desc_en = graphene.String()
    short_desc = graphene.String()
    short_desc_ko = graphene.String()
    short_desc_en = graphene.String()
    background_desc = graphene.String()
    background_desc_ko = graphene.String()
    background_desc_en = graphene.String()
    language = graphene.Field(LanguageNode)
    submitted = graphene.Boolean()
    duration = graphene.Field(DurationNode)
    category_id = graphene.Int()
    difficulty_id = graphene.Int()
    slide_url = graphene.String()
    pdf_url = graphene.String()
    video_url = graphene.String()
    recordable = graphene.Boolean()
    is_presented_before = graphene.Boolean()
    place_presented_before = graphene.String()
    presented_slide_url_before = graphene.String()
    question = graphene.String()


class CreateOrUpdatePresentation(graphene.Mutation):
    presentation = graphene.Field(PresentationNode)

    class Arguments:
        presentation_input = PresentationInput(required=True)

    @login_required
    def mutate(self, info, presentation_input):
        user = info.context.user

        if hasattr(user, 'presentation'):
            presentation = user.presentation
        else:
            presentation = Presentation()
            presentation.owner = user

        if 'category_id' in presentation_input:
            presentation.category = Category.objects.get(
                pk=presentation_input['category_id'])
            del presentation_input['category_id']
        if 'difficulty_id' in presentation_input:
            presentation.difficulty = Difficulty.objects.get(
                pk=presentation_input['difficulty_id'])
            del presentation_input['difficulty_id']

        for k, v in presentation_input.items():
            setattr(presentation, k, v)

        presentation.full_clean()
        presentation.save()
        return CreateOrUpdatePresentation(presentation=presentation)


class UpdatePresentation(graphene.Mutation):
    presentation = graphene.Field(PresentationNode)

    class Arguments:
        id = graphene.Int(required=True)
        presentation_input = PresentationInput(required=True)
        category_id = graphene.Int()
        difficulty_id = graphene.Int()

    @login_required
    def mutate(self, info, presentation_input, category_id=None, difficulty_id=None):
        presentation = Presentation.objects.get(pk=id)
        if category_id:
            presentation.category = Category.objects.get(pk=category_id)
        if difficulty_id:
            presentation.difficulty = Difficulty.objects.get(pk=difficulty_id)

        for k, v in presentation_input.items():
            setattr(presentation, k, v)

        presentation.full_clean()
        presentation.save()
        return UpdatePresentation(presentation=presentation)


class Mutations(graphene.ObjectType):
    create_or_update_presentation = CreateOrUpdatePresentation.Field()


class Query(graphene.ObjectType):
    owner = graphene.Field(UserNode)
    place = graphene.Field(PlaceNode)
    categories = graphene.List(CategoryNode)
    difficulties = graphene.List(DifficultyNode)

    presentations = graphene.List(PresentationNode)
    my_presentation = graphene.Field(PresentationNode)

    def resolve_presentations(self, info):
        condition = Q(accepted=True)
        user = info.context.user
        if user.is_authenticated:
            condition = condition | Q(owner=user)
        return Presentation.objects.filter(condition)

    @login_required
    def resolve_my_presentation(self, info):
        user = info.context.user
        return user.presentation

    def resolve_categories(self, info):
        return Category.objects.filter(visible=True)

    def resolve_difficulties(self, info):
        return Difficulty.objects.all()
