from django.contrib.auth import get_user_model
from django.test import RequestFactory
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.models.sponsor import Sponsor, SponsorLevel
from api.tests.base import BaseTestCase
from api.tests.scheme.sponsor_queries \
    import CREATE_OR_UPDATE_SPONSER, SUBMIT_SPONSOR, SPONSOR_LEVELS


class SponsorTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)
        self.factory = RequestFactory()

    def test_create_or_update_sponsor(self):
        variables = {
            'data': {
                'nameKo': '안 흥미로운 GraphQL',
                'nameEn': 'Not Interesting GraphQL',
                'descKo': 'GraphQL은 재미있다는 설명은함정!',
                'descEn': 'The description that GraphQL is Trap!',
                'managerName': '김스폰서',
                'managerPhone': '0102222222',
                'managerSecondaryPhone': '0103333333',
                'managerEmail': 'sponsor@sponsor.com',
                'levelId': 1,
                'businessRegistrationNumber': '30-3535-3535',
                'contractProcessRequired': True,
                'url': 'my.slide.url'
            }
        }

        # When
        result = self.client.execute(CREATE_OR_UPDATE_SPONSER, variables=variables)
        response_sponsor = result.data['createOrUpdateSponsor']['sponsor']
        self.assertIsNotNone(response_sponsor['id'])

    def test_submit_sponsor(self):
        Sponsor.objects.create(creator=self.user)

        variables = {
            'submitted': True
        }

        # When
        result = self.client.execute(SUBMIT_SPONSOR, variables=variables)

        # Then
        self.assertTrue(result.data['submitSponsor']['submitted'])
        self.assertTrue(result.data['submitSponsor']['success'])
        sponsor = Sponsor.objects.get(creator=self.user)
        self.assertTrue(sponsor.submitted)

    def test_cancel_submit_sponsor(self):
        Sponsor.objects.create(creator=self.user)

        variables = {
            'submitted': False
        }

        # When
        result = self.client.execute(SUBMIT_SPONSOR, variables=variables)

        # Then
        self.assertFalse(result.data['submitSponsor']['submitted'])
        self.assertTrue(result.data['submitSponsor']['success'])
        sponsor = Sponsor.objects.get(creator=self.user)
        self.assertFalse(sponsor.submitted)

    def test_sponsor_level_remaining(self):
        # Given
        sponsor_level = SponsorLevel.objects.get(name_ko='골드')
        Sponsor.objects.create(
            creator=self.user, level=sponsor_level,
            accepted=True, submitted=True)

        # When
        result = self.client.execute(SPONSOR_LEVELS)

        # Then
        response_levels = result.data['sponsorLevels']
        self.assertIsNotNone(response_levels)
        gold_level = [level for level in response_levels if level['nameKo'] == '골드'][0]
        self.assertIsNotNone(gold_level)
        self.assertEqual(gold_level['limit'] - 1, gold_level['currentRemainingNumber'])

    def test_sponsor_level_remaining_two(self):
        # Given
        sponsor_level = SponsorLevel.objects.get(name_ko='골드')
        Sponsor.objects.create(
            creator=self.user, level=sponsor_level,
            accepted=True, submitted=True)
        user2 = get_user_model().objects.create(
            username='user2',
            email='me@pycon.kr')
        Sponsor.objects.create(
            creator=user2, level=sponsor_level,
            accepted=True, submitted=True)

        # When
        result = self.client.execute(SPONSOR_LEVELS)

        # Then
        response_levels = result.data['sponsorLevels']
        self.assertIsNotNone(response_levels)
        gold_level = [level for level in response_levels if level['nameKo'] == '골드'][0]
        self.assertIsNotNone(gold_level)
        self.assertEqual(gold_level['limit'] - 2, gold_level['currentRemainingNumber'])
