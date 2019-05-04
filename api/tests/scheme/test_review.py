from constance import config
from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.models import CFPReview
from api.models.program import Category, Presentation, Difficulty
from api.tests.base import BaseTestCase
from api.tests.scheme.review_queries import ASSIGN_CFP_REVIEWS


class ReviewTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)

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
        category = Category.objects.get(pk=1)
        category2 = Category.objects.get(pk=2)
        difficulty = Difficulty.objects.get(pk=1)
        self.create_presentations(config.CFP_REVIEW_COUNT + 2, category, difficulty)

        variables = {
            'categoryIds': [category.id, category2.id],
            'languages': []
        }

        # When
        result = self.client.execute(ASSIGN_CFP_REVIEWS, variables=variables)
        response = result.data['assignCfpReviews']
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['reviews'])
        self.assertEqual(len(response['reviews']), config.CFP_REVIEW_COUNT)

    def test_WHEN_assign_review_THEN_정의된_개수만큼_리뷰가_할당되고_반환됨2(self):
        category = Category.objects.get(pk=1)
        category2 = Category.objects.get(pk=2)
        difficulty = Difficulty.objects.get(pk=1)
        self.create_presentations(int(config.CFP_REVIEW_COUNT / 2) + 1, category, difficulty)
        self.create_presentations(int(config.CFP_REVIEW_COUNT / 2) + 1, category2, difficulty)

        variables = {
            'categoryIds': [category.id, category2.id],
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
        category = Category.objects.get(pk=1)
        difficulty = Difficulty.objects.get(pk=1)
        category2 = Category.objects.get(pk=2)
        self.create_presentations(presentation_cnt, category, difficulty)

        variables = {
            'categoryIds': [category.id, category2.id],
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
        category = Category.objects.get(pk=1)
        difficulty = Difficulty.objects.get(pk=1)
        category2 = Category.objects.get(pk=2)
        self.create_presentations(presentation_cnt, category, difficulty)

        variables = {
            'categoryIds': [category.id, category2.id],
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

    def create_presentations(self, n, category, difficulty):
        for i in range(n):
            username = f'user_{i}_{category.id}_{difficulty.id}'
            user = get_user_model().objects.create(
                username=username,
                email=f'{username}@pycon.kr')
            Presentation.objects.create(
                name=f'presentation_{i}',
                owner=user,
                background_desc=f'background_{i}',
                duration=Presentation.DURATION_LONG,
                detail_desc=f'detail_desc_{i}',
                category=category,
                difficulty=difficulty,
                submitted=True,
                accepted=True)
