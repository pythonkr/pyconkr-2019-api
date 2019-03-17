from datetime import datetime

import graphene
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required

from api.models.program import Place, Category, Difficulty
from api.models.program import Presentation, PresentationProposal
from api.schemas.user import UserNode


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


class PresentationProposalNode(DjangoObjectType):
    class Meta:
        model = PresentationProposal

    name = graphene.String()
    owner = graphene.Field(UserNode)
    background_desc = graphene.String()
    language = graphene.Field(LanguageNode)
    duration = graphene.Field(DurationNode)
    category = graphene.Field(CategoryNode)
    difficulty = graphene.Field(DifficultyNode)
    recordable = graphene.Boolean()
    is_agreed = graphene.Boolean()

    def resolve_is_agreed(self, info):
        return self.is_agreed_all()


class PresentationProposalInput(graphene.InputObjectType):
    name = graphene.String()
    category_id = graphene.ID()
    difficulty_id = graphene.ID()
    background_desc = graphene.String()
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


class CreateOrUpdatePresentationProposal(graphene.Mutation):
    proposal = graphene.Field(PresentationProposalNode)
    is_agreed_all = graphene.Boolean()

    class Arguments:
        data = PresentationProposalInput(required=True)

    @login_required
    def mutate(self, info, data):
        user = info.context.user
        if hasattr(user, 'presentation'):
            presentation = user.presentation
        else:
            presentation = Presentation()
            presentation.owner = user
            presentation.save()

        if 'category_id' in data:
            presentation.category = Category.objects.get(
                pk=data['category_id'])
            del data['category_id']

        if 'difficulty_id' in data:
            presentation.difficulty = Difficulty.objects.get(
                pk=data['difficulty_id'])
            del data['difficulty_id']
        if 'is_coc_agreed' in data and data['is_coc_agreed']:
            presentation.proposal.coc_agreed_at = datetime.now()
        if 'is_contents_agreed' in data and data['is_contents_agreed']:
            presentation.proposal.contents_agreed_at = datetime.now()
        if 'is_etc_agreed' in data and data['is_etc_agreed']:
            presentation.proposal.etc_agreed_at = datetime.now()
        if hasattr(presentation, 'proposal'):
            proposal = presentation.proposal
        else:
            proposal = PresentationProposal.objects.create(presentation=presentation)
        for k, v in data.items():
            setattr(proposal, k, v)
        presentation.full_clean()
        presentation.save()
        return CreateOrUpdatePresentationProposal(
            proposal=presentation.proposal,
            is_agreed_all=presentation.proposal.is_agreed_all())


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
