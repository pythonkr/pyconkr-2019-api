import graphene
from graphene_django import DjangoObjectType
from api.models.program import Conference


class ConferenceNode(DjangoObjectType):
    class Meta:
        model = Conference
        description = """
        Information of Python Korea Conference.
        """


class Mutations(graphene.ObjectType):
    pass


class Query(graphene.ObjectType):

    conference = graphene.Field(ConferenceNode)

    def resolve_conference(self, info):
        conferences = Conference.objects.all()
        if conferences:
            return conferences[0]
        return None
