from itertools import groupby
from operator import itemgetter
from random import sample

import graphene
from constance import config
from django.db import transaction
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
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
        presentation, created = Presentation.objects.get_or_create(owner=user)

        if created and schedule.presentation_proposal_finish_at and \
                schedule.presentation_proposal_finish_at < now():
            raise GraphQLError(_('발표 제안 기간이 종료되었습니다.'))
        if not schedule.presentation_proposal_start_at or \
                schedule.presentation_proposal_start_at > now():
            raise GraphQLError(_('발표 모집이 아직 시작되지 않았습니다.'))
        if schedule.presentation_review_start_at < now() < schedule.presentation_review_finish_at:
            raise GraphQLError(_('오픈 리뷰 중에는 제안서를 수정할 수 없습니다.'))

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


class AssignCFPReviews(graphene.Mutation):
    reviews = graphene.List(ReviewNode)

    class Arguments:
        category_ids = graphene.List(graphene.ID, required=True)
        languages = graphene.List(LanguageNode)

    @login_required
    def mutate(self, info, category_ids, languages):
        if len(category_ids) < 2:
            raise GraphQLError(_('리뷰할 카테고리를 2개 이상 선택해주어야 합니다.'))
        user = info.context.user
        exist_reviews = CFPReview.objects.filter(owner=user)
        if exist_reviews.count() > 0:
            return AssignCFPReviews(exist_reviews)
        target_presentations = Presentation.objects.filter(submitted=True, category__in=category_ids).exclude(
            owner=user)
        if languages:
            target_presentations = target_presentations.filter(language__in=languages)
        if not target_presentations:
            raise GraphQLError(_('선택한 카테고리에 리뷰할 제안서가 없습니다. 다시 카테고리를 선택해주세요.'))

        reviews = assign_reviews(user, target_presentations)
        return AssignCFPReviews(reviews)


def assign_reviews(user, target_presentations):
    presentations_with_review_cnt = [(p, p.cfp_review_set.count()) for p in target_presentations]
    presentations_with_review_cnt.sort(key=itemgetter(1))
    groups = groupby(presentations_with_review_cnt, itemgetter(1))
    presentations_group_by_review_cnt = [[item[0] for item in data] for (key, data) in groups]
    reviews = []
    for group in presentations_group_by_review_cnt:
        num_of_review_to_assign = config.CFP_REVIEW_COUNT - len(reviews)
        assigned_presentations = group \
            if len(group) <= num_of_review_to_assign \
            else sample(group, num_of_review_to_assign)
        for p in assigned_presentations:
            reviews.append(CFPReview.objects.create(owner=user, presentation=p))
        if len(reviews) is config.CFP_REVIEW_COUNT:
            break
    return reviews


class ReviewInput(graphene.InputObjectType):
    id = graphene.ID()
    comment = graphene.String()


class SubmitCFPReviews(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        reviews = graphene.List(ReviewInput, required=True)

    @transaction.atomic
    @login_required
    def mutate(self, info, reviews):
        user = info.context.user
        schedule = Schedule.objects.last()
        if schedule.presentation_review_finish_at and \
                schedule.presentation_review_finish_at < now():
            raise GraphQLError(_('오픈 리뷰 기간이 종료되었습니다.'))
        if not schedule.presentation_review_start_at or \
                schedule.presentation_review_start_at > now():
            raise GraphQLError(_('오픈 리뷰가 아직 시작되지 않았습니다.'))

        assigned_cnt = CFPReview.objects.filter(owner=user).count()
        if config.CFP_REVIEW_COUNT != len(reviews) or len(reviews) != assigned_cnt:
            raise GraphQLError(_('할당된 리뷰는 한번에 제출되어야 합니다.'))
        for r in reviews:
            review = CFPReview.objects.get(pk=r.id)
            if review.owner != user:
                raise GraphQLError(_('제출된 리뷰가 사용자에게 할당된 리뷰가 아닙니다.'))
            review.comment = r.comment
            review.submitted_at = now()
            review.save()

        return SubmitCFPReviews(success=True)


class Mutations(graphene.ObjectType):
    create_or_update_presentation_proposal = CreateOrUpdatePresentationProposal.Field()
    assign_cfp_reviews = AssignCFPReviews.Field()
    submit_cfp_reviews = SubmitCFPReviews.Field()


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryNode)
    difficulties = graphene.List(DifficultyNode)

    my_presentation_proposal = graphene.Field(PresentationProposalNode)
    assigned_reviews = graphene.List(ReviewNode)
    is_review_submitted = graphene.Boolean()

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
    def resolve_assigned_reviews(self, info):
        user = info.context.user
        return CFPReview.objects.filter(owner=user)

    @login_required
    def resolve_is_review_submitted(self, info):
        user = info.context.user
        is_submitted = False
        for review in CFPReview.objects.filter(owner=user):
            is_submitted = is_submitted or review.submitted
        return is_submitted
