import graphene
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required

from django.db.models import Q
from api.models.program import Presentation, PresentationProposal
from api.models.program import Place, Category, Difficulty
from api.schemas.user import UserNode
from api.schemas.common import SeoulDateTime


class PlaceNode(DjangoObjectType):
    class Meta:
        model = Place
        description = """
        It is the place where the program is held.
        This can be either in the room or in the lobby.
        """


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        description = """
        Category of presentation.
        """


class DifficultyNode(DjangoObjectType):
    class Meta:
        model = Difficulty
        description = """
        Difficulty of presentation.
        """


class LanguageNode(graphene.Enum):
    KOREAN = Presentation.LANGUAGE_KOREAN
    ENGLISH = Presentation.LANGUAGE_ENGLISH


class DurationNode(graphene.Enum):
    SHORT = Presentation.DURATION_SHORT
    LONG = Presentation.DURATION_LONG


class PresentationNode(DjangoObjectType):
    class Meta:
        model = Presentation
        description = """
        Program which speakers present their presentations at Pycon Korea.
        It is one of the the most important program in Pycon Korea.
        """

    language = graphene.Field(LanguageNode)
    duration = graphene.Field(DurationNode)
    started_at = graphene.Field(SeoulDateTime)
    finished_at = graphene.Field(SeoulDateTime)
    created_at = graphene.Field(SeoulDateTime)
    updated_at = graphene.Field(SeoulDateTime)


class PresentationProposalNode(DjangoObjectType):
    class Meta:
        model = PresentationProposal

    owner = graphene.Field(UserNode)
    background_desc = graphene.String()
    duration = graphene.Field(DurationNode)
    category = graphene.Field(CategoryNode)
    difficulty = graphene.Field(DifficultyNode)
    recordable = graphene.Boolean()


class PresentationProposalInput(graphene.InputObjectType):
    name = graphene.String()
    name_ko = graphene.String()
    name_en = graphene.String()
    category_id = graphene.Int()
    difficulty_id = graphene.Int()
    background_desc = graphene.String()
    background_desc_ko = graphene.String()
    background_desc_en = graphene.String()
    language = graphene.Field(LanguageNode)
    duration = graphene.Field(DurationNode)
    submitted = graphene.Boolean()
    detail_desc = graphene.String()
    is_presented_before = graphene.Boolean()
    place_presented_before = graphene.String()
    presented_slide_url_before = graphene.String()
    comment = graphene.String()

    is_coc_agreed = graphene.Boolean()
    is_contents_agreed = graphene.Boolean()
    is_etc_agreed = graphene.Boolean()
    is_proposal_agreed = graphene.Boolean()


class CreateOrUpdatePresentationProposal(graphene.Mutation):
    presentation_proposal = graphene.Field(PresentationProposalNode)
    success = graphene.Boolean()

    class Arguments:
        input = PresentationProposalInput(required=True)

    @login_required
    def mutate(self, info, input):
        user = info.context.user

        if hasattr(user, 'presentation'):
            presentation = user.presentation
        else:
            presentation = Presentation()
            presentation.owner = user
            presentation = presentation.save()

        if 'category_id' in input:
            presentation.category = Category.objects.get(
                pk=input['category_id'])
            del input['category_id']
        if 'difficulty_id' in input:
            presentation.difficulty = Difficulty.objects.get(
                pk=input['difficulty_id'])
            del input['difficulty_id']
        proposal = presentation.proposal
        for k, v in input.items():
            setattr(proposal, k, v)
        presentation.full_clean()
        presentation.save()
        return CreateOrUpdatePresentationProposal(presentation_proposal=presentation.proposal, success=True)


class Mutations(graphene.ObjectType):
    create_or_update_presentation_proposal = CreateOrUpdatePresentationProposal.Field()


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryNode)
    difficulties = graphene.List(DifficultyNode)

    presentation_proposals = graphene.List(PresentationProposalNode)
    my_presentation_proposal = graphene.Field(PresentationProposalNode)

    def resolve_presentation_proposals(self, info):
        return Presentation.objects.filter(submitted=True)

    @login_required
    def resolve_my_presentation_proposal(self, info):
        user = info.context.user
        return user.presentation.proposal

    def resolve_categories(self, info):
        return Category.objects.filter(visible=True)

    def resolve_difficulties(self, info):
        return Difficulty.objects.all()
