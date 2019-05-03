import graphene
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.exceptions import GraphQLError

from api.models import CFPReview
from api.models.program import Place, Category, Difficulty
from api.models.program import Presentation
from api.models.schedule import Schedule
from api.schemas.common import SeoulDateTime
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
        model = Presentation

    owner = graphene.Field(UserNode)
    language = graphene.Field(LanguageNode)
    duration = graphene.Field(DurationNode)
    category = graphene.Field(CategoryNode)
    difficulty = graphene.Field(DifficultyNode)


class ProposalForReviewNode(DjangoObjectType):
    class Meta:
        model = Presentation
        only_fields = ('name', 'name_ko', 'name_en', 'background_desc', 'detail_desc',
                       'language', 'duration', 'category', 'difficulty')
        description = """
        리뷰를 위한 CFP Node입니다. 제안자를 제외하고 리뷰에 필요한 필드만 제공합니다.
        """

    language = graphene.Field(LanguageNode)
    duration = graphene.Field(DurationNode)
    category = graphene.Field(CategoryNode)
    difficulty = graphene.Field(DifficultyNode)


class ReviewNode(DjangoObjectType):
    class Meta:
        model = CFPReview

    presentation = graphene.Field(ProposalForReviewNode)
    submitted_at = graphene.Field(SeoulDateTime)
    submitted = graphene.Boolean()


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


class CreateOrUpdatePresentationProposal(graphene.Mutation):
    proposal = graphene.Field(PresentationProposalNode)

    class Arguments:
        data = PresentationProposalInput(required=True)

    @login_required
    def mutate(self, info, data):
        user = info.context.user
        schedule = Schedule.objects.last()
        is_update = Presentation.objects.filter(owner=user).exists()
        now = timezone.now()
        from django.utils.translation import ugettext_lazy as _
        if is_update and schedule.presentation_proposal_finish_at and \
                schedule.presentation_proposal_finish_at < now:
            raise GraphQLError(_('발표 제안 기간이 종료되었습니다.'))
        if not schedule.presentation_proposal_start_at or \
                schedule.presentation_proposal_start_at > now:
            raise GraphQLError(_('발표 모집이 아직 시작되지 않았습니다.'))
        if schedule.presentation_review_start_at < now < schedule.presentation_review_finish_at:
            raise GraphQLError(_('오픈 리뷰 중에는 제안서를 수정할 수 없습니다.'))

        presentation, _ = Presentation.objects.get_or_create(owner=user)
        if 'category_id' in data:
            presentation.category = Category.objects.get(
                pk=data['category_id'])
            del data['category_id']
        if 'difficulty_id' in data:
            presentation.difficulty = Difficulty.objects.get(
                pk=data['difficulty_id'])
            del data['difficulty_id']
        for k, v in data.items():
            setattr(presentation, k, v)
        presentation.full_clean()
        presentation.save()
        return CreateOrUpdatePresentationProposal(proposal=presentation)


class AssignCFPReview(graphene.Mutation):
    reviews = graphene.List(ReviewNode)

    class Arguments:
        category_ids = graphene.List(graphene.ID, required=True)
        language_ids = graphene.List(graphene.ID, required=True)

    @login_required
    def mutate(self, info, category_ids, language_ids):
        return []


class Mutations(graphene.ObjectType):
    create_or_update_presentation_proposal = CreateOrUpdatePresentationProposal.Field()
    assign_cfp_review = AssignCFPReview.Field()


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryNode)
    difficulties = graphene.List(DifficultyNode)

    my_presentation_proposal = graphene.Field(PresentationProposalNode)
    assigned_reviews = graphene.List(ReviewNode)

    def resolve_categories(self, info):
        return Category.objects.filter(visible=True)

    def resolve_difficulties(self, info):
        return Difficulty.objects.all()

    @login_required
    def resolve_my_presentation_proposal(self, info):
        user = info.context.user
        try:
            return Presentation.objects.get(owner=user)
        except Presentation.DoesNotExist:
            return None

    @login_required
    def resolve_assigned_proposal(self, info):
        user = info.context.user
        return CFPReview.objects.filter(owner=user)
