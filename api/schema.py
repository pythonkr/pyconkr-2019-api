import graphene
from graphene_django import DjangoObjectType
from api.models import Program


class ProgramNode(DjangoObjectType):
    class Meta:
        model = Program


class Query(graphene.ObjectType):
    lists = graphene.List(ProgramNode)

    def resolve_lists(self):
        return Program.objects.all()


# pylint: disable=invalid-name
schema = graphene.Schema(query=Query)
