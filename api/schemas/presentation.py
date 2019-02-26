import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from graphql_extensions.auth.decorators import login_required
from api.models.program import Presentation
from api.models.program import Place, Category, Difficulty
from api.schemas.user import UserNode
from api.schemas.common import SeoulDateTime


class LanguageNode(graphene.Enum):
    KOREAN = 'K'
    ENGLISH = 'E'


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

class PresentationNode(DjangoObjectType):
    class Meta:
        model = Presentation
        description = """
        Program which speakers present their presentations at Pycon Korea.
        It is one of the the most important program in Pycon Korea.
        """
    owner = graphene.Field(UserNode)
    place = graphene.Field(PlaceNode)
    category = graphene.Field(CategoryNode)
    difficulty = graphene.Field(DifficultyNode)
    language = graphene.Field(LanguageNode)
    started_at = graphene.Field(SeoulDateTime)
    finished_at = graphene.Field(SeoulDateTime)

class PresentationInput(graphene.InputObjectType):
    name_ko = graphene.String(required=True)
    name_en = graphene.String()
    desc_ko = graphene.String()
    desc_en = graphene.String()
    language = graphene.Field(LanguageNode)
    submitted = graphene.Boolean()
    slide_url = graphene.String()
    pdf_url = graphene.String()
    video_url = graphene.String()
    recordable = graphene.Boolean()


class CreatePresentation(graphene.Mutation):
    presentation = graphene.Field(PresentationNode)

    class Arguments:
        presentation_input = PresentationInput(required=True)
        category_id = graphene.Int()
        difficulty_id = graphene.Int()

    @login_required
    def mutate(self, info, presentation_input, category_id=None, difficulty_id=None):
        presentation = Presentation()
        presentation.owner = info.context.user
        if category_id:
            presentation.category = Category.objects.get(pk=category_id)
        if difficulty_id:
            presentation.difficulty = Difficulty.objects.get(pk=difficulty_id)

        for k, v in presentation_input.items():
            setattr(presentation, k, v)

        presentation.full_clean()
        presentation.save()
        return CreatePresentation(presentation=presentation)


class Mutations(graphene.ObjectType):
    create_presentation = CreatePresentation.Field()


class Query(graphene.ObjectType):
    presentations = graphene.List(PresentationNode)

    def resolve_presentations(self, info):
        condition = Q(accepted=True)
        user = info.context.user
        if user.is_authenticated:
            condition = condition | Q(owner=user)
        return Presentation.objects.filter(condition)
