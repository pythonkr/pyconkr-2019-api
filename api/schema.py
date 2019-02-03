import datetime
import graphene
import pytz
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from api.models.program import Conference, Program, Presentation
from api.models.program import Place, Category, Difficulty


class SeoulDateTime(graphene.types.Scalar):
    '''
    It is used to replace timezone to Seoul for graphene queries.
    When using the time field, specify scala as follows and return it in Korean time.
    e.g)
    started_at = graphene.Field(SeoulDateTime)
    finished_at = graphene.Field(SeoulDateTime)
    '''

    @staticmethod
    def serialize(obj):
        timezone = pytz.timezone('Asia/Seoul')
        return obj.astimezone(tz=timezone).isoformat()

    @staticmethod
    def parse_literal(node):
        return datetime.datetime.strptime(
            node.value, "%Y-%m-%dT%H:%M:%S.%f")

    @staticmethod
    def parse_value(value):
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        description = "User information"


class ConferenceNode(DjangoObjectType):
    class Meta:
        model = Conference
        description = """
        Information of Python Korea Conference.
        """


class ProgramNode(DjangoObjectType):
    class Meta:
        model = Program
        description = """
        Abstract node for program in Python Conference Korea.
        Many kinds of program inherit this node.
        """


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


class Query(graphene.ObjectType):
    owner = graphene.Field(UserNode)
    conference = graphene.Field(ConferenceNode)
    place = graphene.Field(PlaceNode)
    category = graphene.Field(CategoryNode)
    difficulty = graphene.Field(DifficultyNode)

    programs = graphene.List(ProgramNode)
    presentations = graphene.List(PresentationNode)

    @graphene.resolve_only_args
    def resolve_presentations(self):
        return Presentation.objects.all()

    @graphene.resolve_only_args
    def resolve_conference(self):
        conferences = Conference.objects.all()
        if conferences:
            return conferences[0]
        return None


# pylint: disable=invalid-name
schema = graphene.Schema(query=Query)
