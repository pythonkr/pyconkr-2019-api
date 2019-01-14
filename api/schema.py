# my_django_project/api/schema.py
import graphene
from graphene_django import DjangoObjectType
from api.models import Program

# pylint: disable=too-few-public-methods
class ProgramList(DjangoObjectType):
    class Meta:
        model = Program


class Query(graphene.ObjectType):
    lists = graphene.List(ProgramList)

    @graphene.resolve_only_args
    def resolve_lists(self):
        return ProgramList.objects.all()

# pylint: disable=invalid-name
schema = graphene.Schema(query=Query)
