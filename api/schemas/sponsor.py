import graphene
from graphene_django import DjangoObjectType
from api.models.sponsor import Sponsor, SponsorLevel
from api.schemas.user import UserNode


class SponsorNode(DjangoObjectType):
    class Meta:
        model = Sponsor
        description = """
        Sponsors which spon python conference in Korea.
        """


class SponsorLevelNode(DjangoObjectType):
    class Meta:
        model = SponsorLevel
        description = """
        The level of sponsors, python conference in Korea.
        """


class Mutations(graphene.ObjectType):
    pass


class Query(graphene.ObjectType):
    #owner = graphene.Field(UserNode)
    #sponsorLevel = graphene.List(SponsorLevelNode)

    sponsor = graphene.Field(SponsorNode)
    sponsors = graphene.List(SponsorNode)


    def resolve_sponsor(self, info):
        return Sponsor.objects.all()[0]


    def resolve_sponsors(self, info):
        return Sponsor.objects.all()