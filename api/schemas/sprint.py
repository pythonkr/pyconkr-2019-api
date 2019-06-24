import graphene
from graphene_django import DjangoObjectType

from api.models.program import Sprint


class SprintNode(DjangoObjectType):
    class Meta:
        model = Sprint
        description = """
        Sprint
        """


class Mutations(graphene.ObjectType):
    pass


class Query(graphene.ObjectType):
    sprints = graphene.List(SprintNode)
    sprint = graphene.Field(SprintNode, id=graphene.Int())

    def resolve_sprints(self, info):
        return Sprint.objects.filter(visible=True)

    def resolve_sprint(self, info, id):
        return Sprint.objects.get(pk=id, accepted=True)
