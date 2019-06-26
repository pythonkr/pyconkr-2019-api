import graphene
from graphene_django import DjangoObjectType

from notice.models import Notice


class NoticeNode(DjangoObjectType):
    class Meta:
        model = Notice


class Mutations(graphene.ObjectType):
    pass


class Query(graphene.ObjectType):
    notices = graphene.List(NoticeNode)

    def resolve_notices(self, info):
        return Notice.objects.filter(active=True)
