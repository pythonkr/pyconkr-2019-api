import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from api.models.program import Presentation
from api.models.program import Place, Category, Difficulty
from api.schemas.user import UserNode
from api.schemas.common import SeoulDateTime


class LanguageNode(graphene.Enum):
    KOREAN = 'K'
    ENGLISH = 'E'


class PresentationNode(DjangoObjectType):
    class Meta:
        model = Presentation
        description = """
        Program which speakers present their presentations at Pycon Korea.
        It is one of the the most important program in Pycon Korea.
        """
    language = graphene.Field(LanguageNode)
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
    name_ko = graphene.String(required=True)
    name_en = graphene.String()
    desc_ko = graphene.String()
    desc_en = graphene.String()
    language = graphene.Field(LanguageNode)
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

    def mutate(self, info, presentation_input, category_id=None, difficulty_id=None):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You must be logged to PyCon Korea')

        presentation = Presentation()
        presentation.owner = user
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
    owner = graphene.Field(UserNode)
    place = graphene.Field(PlaceNode)
    category = graphene.Field(CategoryNode)
    difficulty = graphene.Field(DifficultyNode)

    presentations = graphene.List(PresentationNode)

    def resolve_presentations(self, info):
        return Presentation.objects.all()
