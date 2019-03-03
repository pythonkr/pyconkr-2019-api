import graphene
from graphene_django import DjangoObjectType
from api.models.sponsor import Sponsor, SponsorLevel
from api.schemas.common import SeoulDateTime
from api.schemas.profile import UserNode


class SponsorNode(DjangoObjectType):
    class Meta:
        model = Sponsor
        description = """
        Sponsors which spon python conference in Korea.
        """

    paid_at = graphene.Field(SeoulDateTime)


class SponsorLevelNode(DjangoObjectType):
    class Meta:
        model = SponsorLevel
        description = """
        The level of sponsors, python conference in Korea.
        """


class Mutations(graphene.ObjectType):
    pass


class Query(graphene.ObjectType):
    ticketUsers = graphene.List(UserNode)
    sponsorLevel = graphene.Field(SponsorLevelNode)

    sponsor = graphene.Field(SponsorNode)
    sponsors = graphene.List(SponsorNode)

    def resolve_sponsor(self, info):
        return Sponsor.objects.all()[0]

    def resolve_sponsors(self, info):
        return Sponsor.objects.all()
