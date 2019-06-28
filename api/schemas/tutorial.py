import graphene
from graphene_django import DjangoObjectType

from api.models.program import Tutorial
from api.schemas.common import LanguageNode


class TutorialNode(DjangoObjectType):
    class Meta:
        model = Tutorial
        description = """
        Sprint
        """

    language = graphene.Field(LanguageNode)


class Mutations(graphene.ObjectType):
    pass


class Query(graphene.ObjectType):
    tutorials = graphene.List(TutorialNode)
    tutorial = graphene.Field(TutorialNode, id=graphene.Int())

    def resolve_tutorials(self, info):
        return Tutorial.objects.filter(visible=True, accepted=True)

    def resolve_tutorial(self, info, id):
        return Tutorial.objects.get(pk=id, accepted=True)
