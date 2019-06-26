import graphene
from graphene_django import DjangoObjectType

from api.models.program import Sprint
from api.schemas.common import SeoulDateTime, PlaceNode
from api.schemas.user import UserNode


class SprintNode(DjangoObjectType):
    class Meta:
        model = Sprint
        description = """
        Sprint
        """

    place = graphene.Field(PlaceNode)
    owner = graphene.Field(UserNode)
    started_at = graphene.Field(SeoulDateTime)
    finished_at = graphene.Field(SeoulDateTime)


class Mutations(graphene.ObjectType):
    pass


class Query(graphene.ObjectType):
    sprints = graphene.List(SprintNode)
    sprint = graphene.Field(SprintNode, id=graphene.Int())

    def resolve_sprints(self, info):
        return Sprint.objects.filter(accepted=True)

    def resolve_sprint(self, info, id):
        return Sprint.objects.get(pk=id, accepted=True)
