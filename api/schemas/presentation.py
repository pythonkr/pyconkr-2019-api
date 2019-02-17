import graphene
from graphene_django import DjangoObjectType
from api.models.program import Presentation
from api.models.program import Place, Category, Difficulty
from api.schemas.user import UserNode
from api.schemas.common import SeoulDateTime


class PresentationNode(DjangoObjectType):
    class Meta:
        model = Presentation
        description = """
        Program which speakers present their presentations at Pycon Korea.
        It is one of the the most important program in Pycon Korea.
        """
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


class Mutations(graphene.ObjectType):
    pass


class Query(graphene.ObjectType):
    owner = graphene.Field(UserNode)
    place = graphene.Field(PlaceNode)
    category = graphene.Field(CategoryNode)
    difficulty = graphene.Field(DifficultyNode)

    presentations = graphene.List(PresentationNode)

    def resolve_presentations(self, info):
        return Presentation.objects.all()
