import graphene
from django.utils.translation import ugettext_lazy as _
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.exceptions import GraphQLError

from api.models.program import Tutorial
from api.schemas.common import LanguageNode, PlaceNode, SeoulDateTime, UserEmailNode
from api.schemas.user import UserNode
from ticket.models import Ticket


class TutorialNode(DjangoObjectType):
    class Meta:
        model = Tutorial
        description = """
        Sprint
        """

    language = graphene.Field(LanguageNode)
    place = graphene.Field(PlaceNode)
    owner = graphene.Field(UserNode)
    started_at = graphene.Field(SeoulDateTime)
    finished_at = graphene.Field(SeoulDateTime)
    participants = graphene.List(UserEmailNode)

    def resolve_participants(self, info):
        user = info.context.user
        if not self.has_owner_permission(user, self.owner):
            return None
        tickets = self.ticket_product.ticket_set.filter(status=Ticket.STATUS_PAID)
        return [t.owner.profile for t in tickets]

    def has_owner_permission(self, user, owner):
        if user.is_staff or user.is_superuser:
            return True
        if owner and owner is user:
            return True
        if user.profile and user.profile.is_organizer:
            return True
        return False


class TutorialInput(graphene.InputObjectType):
    desc_ko = graphene.String()
    desc_en = graphene.String()


class UpdateTutorial(graphene.Mutation):
    tutorial = graphene.Field(TutorialNode)

    class Arguments:
        id = graphene.Int()
        data = TutorialInput(required=True)

    @login_required
    def mutate(self, info, id, data):
        user = info.context.user
        try:
            if id:
                tutorial = Tutorial.objects.get(pk=id, owner=user, accepted=True)
            else:
                tutorial = Tutorial.objects.last(owner=user, accepted=True)
            for k, v in data.items():
                setattr(tutorial, k, v)
            tutorial.save()
            return UpdateTutorial(tutorial=tutorial)
        except Tutorial.DoesNotExist:
            raise GraphQLError(_('튜토리얼 진행자가 아닙니다. '
                                 '문제가 있을 경우 파이콘 한국 준비위원회에게 문의 부탁드립니다.'))


class Mutations(graphene.ObjectType):
    update_tutorial = UpdateTutorial.Field()


class Query(graphene.ObjectType):
    tutorials = graphene.List(TutorialNode)
    tutorial = graphene.Field(TutorialNode, id=graphene.Int())
    my_tutorials = graphene.List(TutorialNode)

    def resolve_tutorials(self, info):
        return Tutorial.objects.filter(visible=True, accepted=True)

    def resolve_tutorial(self, info, id):
        return Tutorial.objects.get(pk=id, accepted=True)

    @login_required
    def resolve_my_tutorials(self, info):
        return Tutorial.objects.filter(owner=info.context.user)
