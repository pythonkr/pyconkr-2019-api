import graphene
from django.utils.translation import ugettext_lazy as _
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.exceptions import GraphQLError

from api.models.program import Tutorial, YoungCoder
from api.schemas.common import LanguageNode, PlaceNode, SeoulDateTime
from api.schemas.user import UserNode


class YoungCoderNode(DjangoObjectType):
    class Meta:
        model = YoungCoder
        description = """
        YoungCoder
        """


class Mutations(graphene.ObjectType):
    pass


class Query(graphene.ObjectType):
    youngCoders = graphene.List(YoungCoderNode)
    youngCoder = graphene.Field(YoungCoderNode, id=graphene.Int())

    def resolve_young_coders(self, info):
        return YoungCoder.objects.filter(visible=True, accepted=True)

    def resolve_young_coder(self, info, id):
        return YoungCoder.objects.get(pk=id, accepted=True)
