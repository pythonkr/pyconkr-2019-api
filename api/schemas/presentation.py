from itertools import groupby
from operator import itemgetter
from random import sample

import graphene
from constance import config
from django.db import transaction
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.exceptions import GraphQLError

from api.models import CFPReview
from api.models.program import Category, Difficulty
from api.models.program import Presentation
from api.models.schedule import Schedule
from api.schemas.common import SeoulDateTime, LanguageNode, DifficultyNode, has_owner_permission
from api.schemas.user import UserNode


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        description = """
        Category of presentation.
        """


class DurationNode(graphene.Enum):
    SHORT = Presentation.DURATION_SHORT
    LONG = Presentation.DURATION_LONG


class PresentationProposalNode(DjangoObjectType):
    class Meta:
        model = Presentation
        description = """
        제안서를 위한 노드입니다. 
        공개되지 않는 몇몇 필드들이 포함되어 있기 때문에 당사자가 아니라면 조회할 수 없어야 합니다.
        """

    owner = graphene.Field(UserNode)
    language = graphene.Field(LanguageNode)
    duration = graphene.Field(DurationNode)
    category = graphene.Field(CategoryNode)
    difficulty = graphene.Field(DifficultyNode)


class PublicPresentationNode(DjangoObjectType):
    class Meta:
        model = Presentation
        exclude_fields = ('detail_desc', 'is_presented_before', 'place_presented_before',
                          'presented_slide_url_before', 'comment', '')
        description = """
        공개되는 발표 정보입니다.
        """

    owner = graphene.Field(UserNode)
    secondary_owner = graphene.Field(UserNode)
    language = graphene.Field(LanguageNode)
    duration = graphene.Field(DurationNode)
    category = graphene.Field(CategoryNode)
    difficulty = graphene.Field(DifficultyNode)
    slide_url = graphene.String()
    desc = graphene.String()

    def resolve_desc(self, info):
        if self.desc:
            return self.desc
        return self.detail_desc

    def resolve_slide_url(self, info):
        if timezone.now() > self.finished_at:
            return self.slide_url
        if has_owner_permission(info.context.user, self.owner):
            return self.slide_url
        return ''


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


class CFPReviewNode(DjangoObjectType):
    class Meta:
        model = CFPReview

    presentation = graphene.Field(ProposalForReviewNode)
    submitted_at = graphene.Field(SeoulDateTime)
    submitted = graphene.Boolean()
    comment = graphene.String()
    owner = graphene.Field(UserNode)

    def resolve_comment(self, info):
        if has_owner_permission(info.context.user, self.owner):
            return self.comment
        return ''

    def resolve_owner(self, info):
        if has_owner_permission(info.context.user, self.owner):
            return self.owner
        return None


class PresentationProposalInput(graphene.InputObjectType):
    name = graphene.String()
    name_ko = graphene.String()
    name_en = graphene.String()
    desc = graphene.String()
    desc_ko = graphene.String()
    desc_en = graphene.String()
    category_id = graphene.ID()
    difficulty_id = graphene.ID()
    slide_url = graphene.String()
    video_url = graphene.String()
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
    reviews = graphene.List(CFPReviewNode)

    class Arguments:
        category_ids = graphene.List(graphene.ID, required=True)

    @login_required
    def mutate(self, info, category_ids):
        if len(category_ids) < 2:
            raise GraphQLError(_('리뷰할 카테고리를 2개 이상 선택해주어야 합니다.'))
        user = info.context.user
        exist_reviews = CFPReview.objects.filter(owner=user)
        if exist_reviews.count() > 0:
            return AssignCFPReviews(exist_reviews)
        target_presentations = Presentation.objects.filter(submitted=True, category__in=category_ids).exclude(
            owner=user)
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
        if len(reviews) != assigned_cnt:
            raise GraphQLError(_('할당된 리뷰는 한번에 제출되어야 합니다.'))
        for r in reviews:
            review = CFPReview.objects.get(pk=r.id)
            if review.owner != user:
                raise GraphQLError(_('제출된 리뷰가 사용자에게 할당된 리뷰가 아닙니다.'))
            review.comment = r.comment
            review.submitted_at = now()
            review.submitted = True
            review.save()

        return SubmitCFPReviews(success=True)


class Mutations(graphene.ObjectType):
    create_or_update_presentation_proposal = CreateOrUpdatePresentationProposal.Field()
    assign_cfp_reviews = AssignCFPReviews.Field()
    submit_cfp_reviews = SubmitCFPReviews.Field()


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryNode)
    difficulties = graphene.List(DifficultyNode)
    presentations = graphene.List(PublicPresentationNode)
    presentation = graphene.Field(PublicPresentationNode, id=graphene.Int())

    my_presentation_proposal = graphene.Field(PresentationProposalNode)
    assigned_cfp_reviews = graphene.List(CFPReviewNode)
    is_cfp_review_submitted = graphene.Boolean()

    def resolve_categories(self, info):
        return Category.objects.filter(visible=True)

    def resolve_difficulties(self, info):
        return Difficulty.objects.all()

    def resolve_presentations(self, info):
        return Presentation.objects.filter(accepted=True)

    def resolve_presentation(self, info, id):
        return Presentation.objects.get(pk=id, accepted=True)

    @login_required
    def resolve_my_presentation_proposal(self, info):
        user = info.context.user
        try:
            return Presentation.objects.get(owner=user)
        except Presentation.DoesNotExist:
            return None

    @login_required
    def resolve_assigned_cfp_reviews(self, info):
        user = info.context.user
        return CFPReview.objects.filter(owner=user)

    @login_required
    def resolve_is_cfp_review_submitted(self, info):
        user = info.context.user
        for review in CFPReview.objects.filter(owner=user):
            if review.submitted:
                return True
        return False
