import graphene
from django.utils.translation import ugettext_lazy as _
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.exceptions import GraphQLError

from api.models.program import Sprint
from api.schemas.common import SeoulDateTime, PlaceNode, LanguageNode, UserEmailNode, has_owner_permission
from api.schemas.user import UserNode
from ticket.models import Ticket


class SprintNode(DjangoObjectType):
    class Meta:
        model = Sprint
        description = """
        Sprint
        """

    place = graphene.Field(PlaceNode)
    owner = graphene.Field(UserNode)
    language = graphene.Field(LanguageNode)
    started_at = graphene.Field(SeoulDateTime)
    finished_at = graphene.Field(SeoulDateTime)
    participants = graphene.List(UserEmailNode)

    def resolve_participants(self, info):
        user = info.context.user
        if not has_owner_permission(user, self.owner):
            return None
        if not self.ticket_product:
            return None
        tickets = self.ticket_product.ticket_set.filter(status=Ticket.STATUS_PAID)
        return [t.owner.profile for t in tickets]


class SprintInput(graphene.InputObjectType):
    desc_ko = graphene.String()
    desc_en = graphene.String()


class UpdateSprint(graphene.Mutation):
    sprint = graphene.Field(SprintNode)

    class Arguments:
        id = graphene.Int()
        data = SprintInput(required=True)

    @login_required
    def mutate(self, info, id, data):
        user = info.context.user
        try:
            if id:
                sprint = Sprint.objects.get(pk=id, owner=user, accepted=True)
            else:
                sprint = Sprint.objects.last(owner=user, accepted=True)
            for k, v in data.items():
                setattr(sprint, k, v)
            sprint.save()
            return UpdateSprint(sprint=sprint)
        except Sprint.DoesNotExist:
            raise GraphQLError(_('스프린트 진행자가 아닙니다. '
                                 '문제가 있을 경우 파이콘 한국 준비위원회에게 문의 부탁드립니다.'))


class Mutations(graphene.ObjectType):
    update_sprint = UpdateSprint.Field()


class Query(graphene.ObjectType):
    sprints = graphene.List(SprintNode)
    sprint = graphene.Field(SprintNode, id=graphene.Int())
    my_sprints = graphene.List(SprintNode)

    def resolve_sprints(self, info):
        return Sprint.objects.filter(accepted=True)

    def resolve_sprint(self, info, id):
        return Sprint.objects.get(pk=id, accepted=True)

    @login_required
    def resolve_my_sprints(self, info):
        return Sprint.objects.filter(owner=info.context.user)
