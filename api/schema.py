import graphene
from graphene import Schema, resolve_only_args
from graphene_django import DjangoObjectType
from api.models.programs import Presentation


class PresentationNode(DjangoObjectType):
    class Meta:
        model = Presentation


class Query(graphene.ObjectType):
    presentations = graphene.List(PresentationNode)

    @resolve_only_args
    def resolve_presentations(self):
        return Presentation.objects.all()


# pylint: disable=invalid-name
schema = Schema(query=Query)
