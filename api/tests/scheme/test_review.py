from datetime import timedelta

from constance import config
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.models import CFPReview
from api.models.program import Category, Presentation, Difficulty
from api.models.schedule import Schedule
from api.tests.base import BaseTestCase
from api.tests.scheme.review_queries import ASSIGN_CFP_REVIEWS, SUBMIT_CFP_REVIEWS, ASSIGNED_CFP_REVIEWS


class ReviewTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)
        self.category = Category.objects.get(pk=1)
        self.category2 = Category.objects.get(pk=2)
        self.difficulty = Difficulty.objects.get(pk=1)

    def set_openreview_period(self):
        schedule = Schedule.objects.last()
        schedule.presentation_review_start_at = now() - timedelta(days=2)
        schedule.presentation_review_finish_at = now() + timedelta(days=2)
        schedule.save()

    def test_GIVEN_category_ids_empty_WHEN_assign_review_THEN_throw_exception(self):
        variables = {
            'categoryIds': [],
            'languages': []
        }

        # When
        result = self.client.execute(ASSIGN_CFP_REVIEWS, variables=variables)
        self.assertIsNotNone(result.errors)

    def test_GIVEN_category_ids_one_WHEN_assign_review_THEN_throw_exception(self):
        variables = {
            'categoryIds': ['1'],
            'languages': []
        }

        # When
        result = self.client.execute(ASSIGN_CFP_REVIEWS, variables=variables)
        self.assertIsNotNone(result.errors)

    def test_GIVEN_제안서가_없으면_WHEN_assign_review_THEN_throw_exception(self):
        variables = {
            'categoryIds': ['1', '2'],
            'languages': []
        }

        # When
        result = self.client.execute(ASSIGN_CFP_REVIEWS, variables=variables)
        self.assertIsNotNone(result.errors)

    def test_WHEN_assign_review_THEN_정의된_개수만큼_리뷰가_할당되고_반환됨(self):
        self.create_presentations(config.CFP_REVIEW_COUNT + 2, self.category, self.difficulty)

        variables = {
            'categoryIds': [self.category.id, self.category2.id],
            'languages': []
        }

        # When
        result = self.client.execute(ASSIGN_CFP_REVIEWS, variables=variables)
        response = result.data['assignCfpReviews']
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['reviews'])
        self.assertEqual(len(response['reviews']), config.CFP_REVIEW_COUNT)

    def test_WHEN_assign_review_THEN_정의된_개수만큼_리뷰가_할당되고_반환됨2(self):
        self.create_presentations(int(config.CFP_REVIEW_COUNT / 2) + 1, self.category, self.difficulty)
        self.create_presentations(int(config.CFP_REVIEW_COUNT / 2) + 1, self.category2, self.difficulty)

        variables = {
            'categoryIds': [self.category.id, self.category2.id],
            'languages': []
        }

        # When
        result = self.client.execute(ASSIGN_CFP_REVIEWS, variables=variables)
        response = result.data['assignCfpReviews']
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['reviews'])
        self.assertEqual(len(response['reviews']), config.CFP_REVIEW_COUNT)

    def test_GIVEN_정의된_개수_이하의_제안서가_있을_경우_WHEN_assign_review_THEN_있는만큼만_리뷰가_할당되고_반환됨(self):
        # Given
        presentation_cnt = config.CFP_REVIEW_COUNT - 1
        self.create_presentations(presentation_cnt, self.category, self.difficulty)

        variables = {
            'categoryIds': [self.category.id, self.category2.id],
            'languages': []
        }

        # When
        result = self.client.execute(ASSIGN_CFP_REVIEWS, variables=variables)

        # Then
        response = result.data['assignCfpReviews']
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['reviews'])
        self.assertEqual(len(response['reviews']), presentation_cnt)

    def test_GIVEN_WHEN_두_번_assign_review_호출해도_THEN_새로운_리뷰가_할당되지_않음(self):
        # Given
        presentation_cnt = config.CFP_REVIEW_COUNT * 3
        self.create_presentations(presentation_cnt, self.category, self.difficulty)

        variables = {
            'categoryIds': [self.category.id, self.category2.id],
            'languages': []
        }

        # When
        self.client.execute(ASSIGN_CFP_REVIEWS, variables=variables)
        result = self.client.execute(ASSIGN_CFP_REVIEWS, variables=variables)

        # Then
        response = result.data['assignCfpReviews']
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['reviews'])
        self.assertEqual(len(response['reviews']), config.CFP_REVIEW_COUNT)
        self.assertEqual(CFPReview.objects.filter(owner=self.user).count(), config.CFP_REVIEW_COUNT)

    def test_GIVEN_WHEN_submit_cfp_review_THEN_submit_처리됨(self):
        # Given
        presentation_cnt = config.CFP_REVIEW_COUNT * 3
        presentations = self.create_presentations(presentation_cnt, self.category, self.difficulty)
        reviews = self.create_reviews(self.user, presentations[:config.CFP_REVIEW_COUNT])
        reviews_variable = [{'id': r.id, 'comment': f'{r.presentation.name}_comment'} for r in reviews]
        variables = {
            'reviews': reviews_variable
        }

        # When
        result = self.client.execute(SUBMIT_CFP_REVIEWS, variables=variables)

        # Then
        response = result.data['submitCfpReviews']
        self.assertIsNotNone(response)
        self.assertTrue(response['success'])
        for r in CFPReview.objects.filter(owner=self.user):
            self.assertIsNotNone(r.submitted_at)
            self.assertTrue(r.submitted)
            self.assertIsNotNone(r.comment)
            self.assertNotEqual('', r.comment)

    def test_GIVEN_다른유저의_Review에_submit하면_WHEN_submit_cfp_review_THEN_에러_발생(self):
        # Given
        presentation_cnt = config.CFP_REVIEW_COUNT * 3
        presentations = self.create_presentations(presentation_cnt, self.category, self.difficulty)
        cfp_count_cnt = config.CFP_REVIEW_COUNT
        reviews = self.create_reviews(self.user, presentations[:cfp_count_cnt])
        other_user = get_user_model().objects.create(
            username='other_user',
            email='other_user@pycon.kr')
        other_reviews = self.create_reviews(other_user, presentations[cfp_count_cnt:cfp_count_cnt * 2])
        reviews = reviews[:-1] + other_reviews[:1]
        reviews_variable = [{'id': r.id, 'comment': f'{r.presentation.name}_comment'} for r in reviews]
        variables = {
            'reviews': reviews_variable
        }

        # When
        result = self.client.execute(SUBMIT_CFP_REVIEWS, variables=variables)

        # Then
        self.assertIsNotNone(result.errors)

    def test_GIVEN_할당된_리뷰를_한번에_모두_제출하지_않으면_WHEN_submit_cfp_review_THEN_에러_발생(self):
        # Given
        presentation_cnt = config.CFP_REVIEW_COUNT * 3
        presentations = self.create_presentations(presentation_cnt, self.category, self.difficulty)
        reviews = self.create_reviews(self.user, presentations[:config.CFP_REVIEW_COUNT])
        reviews_variable = [{'id': r.id, 'comment': f'{r.presentation.name}_comment'} for r in reviews[:-1]]
        variables = {
            'reviews': reviews_variable
        }

        # When
        result = self.client.execute(SUBMIT_CFP_REVIEWS, variables=variables)

        # Then
        self.assertIsNotNone(result.errors)

    def test_GIVEN_오픈리뷰_기간_전에는_WHEN_submit_cfp_review_THEN_에러_발생(self):
        # Given
        schedule = Schedule.objects.last()
        schedule.presentation_review_start_at = now() + timedelta(days=1)
        schedule.presentation_review_finish_at = now() + timedelta(days=4)
        schedule.save()

        presentation_cnt = config.CFP_REVIEW_COUNT * 3
        presentations = self.create_presentations(presentation_cnt, self.category, self.difficulty)
        reviews = self.create_reviews(self.user, presentations[:config.CFP_REVIEW_COUNT])
        reviews_variable = [{'id': r.id, 'comment': f'{r.presentation.name}_comment'} for r in reviews]
        variables = {
            'reviews': reviews_variable
        }

        # When
        result = self.client.execute(SUBMIT_CFP_REVIEWS, variables=variables)

        # Then
        self.assertIsNotNone(result.errors)

    def test_GIVEN_오픈리뷰_기간이_지나면_WHEN_submit_cfp_review_THEN_에러_발생(self):
        # Given
        schedule = Schedule.objects.last()
        schedule.presentation_review_start_at = now() - timedelta(days=6)
        schedule.presentation_review_finish_at = now() - timedelta(days=2)
        schedule.save()

        presentation_cnt = config.CFP_REVIEW_COUNT * 3
        presentations = self.create_presentations(presentation_cnt, self.category, self.difficulty)
        reviews = self.create_reviews(self.user, presentations[:config.CFP_REVIEW_COUNT])
        reviews_variable = [{'id': r.id, 'comment': f'{r.presentation.name}_comment'} for r in reviews]
        variables = {
            'reviews': reviews_variable
        }

        # When
        result = self.client.execute(SUBMIT_CFP_REVIEWS, variables=variables)

        # Then
        self.assertIsNotNone(result.errors)

    def test_WHEN_assigned_reviews_THEN_정상적으로_반환(self):
        # Given
        presentations = self.create_presentations(config.CFP_REVIEW_COUNT, self.category, self.difficulty)
        reviews = self.create_reviews(self.user, presentations)

        # When
        result = self.client.execute(ASSIGNED_CFP_REVIEWS)

        # Then
        self.assertFalse(result.data['isCfpReviewSubmitted'])
        self.assertIsNotNone(result.data['assignedCfpReviews'])
        self.assertEqual(len(reviews), len(result.data['assignedCfpReviews']))

    def test_GIVEN_제출한_이후에는_WHEN_assigned_reviews_THEN_정상적으로_반환되고_is_submitted도_true(self):
        # Given
        presentations = self.create_presentations(config.CFP_REVIEW_COUNT, self.category, self.difficulty)
        reviews = self.create_reviews(self.user, presentations, submitted=True)

        # When
        result = self.client.execute(ASSIGNED_CFP_REVIEWS)

        # Then
        self.assertTrue(result.data['isCfpReviewSubmitted'])
        self.assertIsNotNone(result.data['assignedCfpReviews'])
        self.assertEqual(len(reviews), len(result.data['assignedCfpReviews']))

    def create_reviews(self, user, presentations, submitted=False):
        reviews = []
        for p in presentations:
            review = CFPReview(owner=user, presentation=p)
            if submitted:
                review.submitted_at = now()
                review.submitted = True
                review.comment = f'{p.name}_comment'
            review.save()
            reviews.append(review)
        return reviews

    def create_presentations(self, n, category, difficulty):
        presentations = []
        for i in range(n):
            username = f'user_{i}_{category.id}_{difficulty.id}'
            user = get_user_model().objects.create(
                username=username,
                email=f'{username}@pycon.kr')
            presentations.append(Presentation.objects.create(
                name=f'presentation_{i}',
                owner=user,
                background_desc=f'background_{i}',
                duration=Presentation.DURATION_LONG,
                detail_desc=f'detail_desc_{i}',
                category=category,
                difficulty=difficulty,
                submitted=True,
                accepted=True))
        return presentations
