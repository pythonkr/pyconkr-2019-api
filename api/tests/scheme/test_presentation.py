from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone, now
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.models.program import Presentation
from api.models.schedule import Schedule
from api.tests.base import BaseTestCase
from api.tests.scheme.presentation_queries import CREATE_OR_UPDATE_PRESENTATION_PROPOSAL

TIMEZONE = get_current_timezone()

UserModel = get_user_model()


class PresentationTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)
        self.set_proposal_period()

    def set_proposal_period(self):
        schedule = Schedule.objects.last()
        schedule.presentation_proposal_start_at = now() - timedelta(days=2)
        schedule.presentation_proposal_finish_at = now() + timedelta(days=2)
        schedule.presentation_review_start_at = now() + timedelta(days=4)
        schedule.presentation_review_finish_at = now() + timedelta(days=20)
        schedule.save()

    def test_create_proposal(self):
        variables = {
            'data': {
                'name': '흥미로운 GraphQL',
                'backgroundDesc': '자바',
                'detailDesc': 'GraphQL은 재미있다는 설명!',
                'language': 'KOREAN',
                'duration': 'SHORT',
                'isPresentedBefore': True,
                'placePresentedBefore': '학교 강당 앞',
                'presentedSlideUrlBefore': 'my.previous.url',
                'comment': '밥은 주시는거죠?',
                'submitted': True,
            }
        }

        response = self.client.execute(CREATE_OR_UPDATE_PRESENTATION_PROPOSAL, variables)
        data = response.data
        self.assertIsNotNone(data['createOrUpdatePresentationProposal'])
        self.assertIsNotNone(data['createOrUpdatePresentationProposal']['proposal'])

    def test_update_proposal_first_step(self):
        variables = {
            'data': {
                'name': '흥미로운 GraphQL',
                'categoryId': 2,
                'difficultyId': 2,
                'backgroundDesc': '자바',
                'duration': 'LONG',
                'language': 'ENGLISH',
            }
        }

        response = self.client.execute(CREATE_OR_UPDATE_PRESENTATION_PROPOSAL, variables)
        data = response.data
        self.assertIsNotNone(data['createOrUpdatePresentationProposal'])
        self.assertIsNotNone(data['createOrUpdatePresentationProposal']['proposal'])
        proposal = data['createOrUpdatePresentationProposal']['proposal']
        self.assertEqual(proposal['name'], '흥미로운 GraphQL')
        self.assertEqual(proposal['category']['id'], '2')
        self.assertEqual(proposal['difficulty']['id'], '2')
        self.assertEqual(proposal['backgroundDesc'], '자바')
        self.assertEqual(proposal['duration'], 'LONG')
        self.assertEqual(proposal['language'], 'ENGLISH')

        self.assertEqual(self.user.presentation.name, '흥미로운 GraphQL')
        self.assertEqual(self.user.presentation.category.id, 2)
        self.assertEqual(self.user.presentation.difficulty.id, 2)
        self.assertEqual(self.user.presentation.background_desc, '자바')
        self.assertEqual(self.user.presentation.duration, Presentation.DURATION_LONG)
        self.assertEqual(self.user.presentation.language, Presentation.LANGUAGE_ENGLISH)

    def test_update_proposal_second_step(self):
        Presentation.objects.create(owner=self.user, name='흥미로운 GraphQL')
        detail_desc = '이번 CFP에서 제안하고 싶은 내용은 1) graphQL 쓰세요 2) 자동 베포 좋아요 입니다'
        place_presented_before = '우리 학교'
        presented_slide_url_before = 'http://url.com'
        comment = '밥은 주시는거죠?'

        variables = {
            'data': {
                'detailDesc': detail_desc,
                'isPresentedBefore': True,
                'placePresentedBefore': place_presented_before,
                'presentedSlideUrlBefore': presented_slide_url_before,
                'comment': comment
            }
        }

        response = self.client.execute(CREATE_OR_UPDATE_PRESENTATION_PROPOSAL, variables)
        data = response.data
        self.assertIsNotNone(data['createOrUpdatePresentationProposal'])
        self.assertIsNotNone(data['createOrUpdatePresentationProposal']['proposal'])
        proposal = data['createOrUpdatePresentationProposal']['proposal']
        self.assertEqual(proposal['detailDesc'], detail_desc)
        self.assertEqual(proposal['isPresentedBefore'], True)
        self.assertEqual(proposal['placePresentedBefore'], place_presented_before)
        self.assertEqual(proposal['presentedSlideUrlBefore'], presented_slide_url_before)

        presentation = Presentation.objects.get(owner=self.user)
        self.assertEqual(presentation.detail_desc, detail_desc)
        self.assertEqual(presentation.is_presented_before, True)
        self.assertEqual(presentation.place_presented_before, place_presented_before)
        self.assertEqual(presentation.presented_slide_url_before, presented_slide_url_before)

    def test_update_proposal_submit(self):
        Presentation.objects.create(owner=self.user, name='흥미로운 GraphQL')

        variables = {
            'data': {
                'submitted': True,
            }
        }

        response = self.client.execute(CREATE_OR_UPDATE_PRESENTATION_PROPOSAL, variables)
        data = response.data
        self.assertIsNotNone(data['createOrUpdatePresentationProposal'])
        self.assertIsNotNone(data['createOrUpdatePresentationProposal']['proposal'])

        presentation = Presentation.objects.get(owner=self.user)
        self.assertTrue(presentation.submitted)
