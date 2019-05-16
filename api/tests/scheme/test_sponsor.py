from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.utils.timezone import now
from graphql_jwt.testcases import JSONWebTokenTestCase
from graphql_relay import to_global_id

from api.models.sponsor import Sponsor, SponsorLevel
from api.schemas.sponsor import PublicSponsorNode
from api.tests.base import BaseTestCase
from api.tests.scheme.sponsor_queries \
    import CREATE_OR_UPDATE_SPONSER, SUBMIT_SPONSOR, SPONSOR_LEVELS, MY_SPONSOR, SPONSORS, SPONSOR


class SponsorTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)
        self.factory = RequestFactory()

    def test_후원사_등록_이력이_없을_때에는_None_반환(self):
        result = self.client.execute(MY_SPONSOR)
        self.assertIsNone(result.data['mySponsor'])

    def test_후원사_등록_이력이_있을_때에는_정상적으로_반환(self):
        Sponsor.objects.create(name='스폰서사', creator=self.user)
        result = self.client.execute(MY_SPONSOR)
        self.assertIsNotNone(result.data['mySponsor'])

    def test_create_or_update_sponsor(self):
        variables = {
            'data': {
                'nameKo': '안 흥미로운 GraphQL',
                'nameEn': 'Not Interesting GraphQL',
                'descKo': 'GraphQL은 재미있다는 설명은함정!',
                'descEn': 'The description that GraphQL is Trap!',
                'managerName': '김스폰서',
                'managerEmail': 'sponsor@sponsor.com',
                'levelId': 1,
                'businessRegistrationNumber': '30-3535-3535',
                'url': 'my.slide.url'
            }
        }

        # When
        result = self.client.execute(CREATE_OR_UPDATE_SPONSER, variables=variables)
        response_sponsor = result.data['createOrUpdateSponsor']['sponsor']
        self.assertIsNotNone(response_sponsor['id'])

    def test_create_or_update_sponsor_남은_구좌가_없으면_에러_발생(self):
        level = SponsorLevel.objects.get(pk=1)
        level.limit = 0
        level.save()

        variables = {
            'data': {
                'nameKo': '안 흥미로운 GraphQL',
                'nameEn': 'Not Interesting GraphQL',
                'descKo': 'GraphQL은 재미있다는 설명은함정!',
                'descEn': 'The description that GraphQL is Trap!',
                'managerName': '김스폰서',
                'managerEmail': 'sponsor@sponsor.com',
                'levelId': 1,
                'businessRegistrationNumber': '30-3535-3535',
                'url': 'my.slide.url'
            }
        }

        # When
        result = self.client.execute(CREATE_OR_UPDATE_SPONSER, variables=variables)
        self.assertIsNotNone(result.errors)

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

    def test_sponsor_level_remaining_accepted만_되었을때도_줄어들어야_한다(self):
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

    def test_sponsor_level_remaining(self):
        # Given
        sponsor_level = SponsorLevel.objects.get(name_ko='골드')
        Sponsor.objects.create(
            creator=self.user, level=sponsor_level,
            accepted=True, submitted=True, paid_at=now())

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
            accepted=True, submitted=True, paid_at=now())
        user2 = get_user_model().objects.create(
            username='user2',
            email='me@pycon.kr')
        Sponsor.objects.create(
            creator=user2, level=sponsor_level,
            accepted=True, submitted=True, paid_at=now())

        # When
        result = self.client.execute(SPONSOR_LEVELS)

        # Then
        response_levels = result.data['sponsorLevels']
        self.assertIsNotNone(response_levels)
        gold_level = [level for level in response_levels if level['nameKo'] == '골드'][0]
        self.assertIsNotNone(gold_level)
        self.assertEqual(gold_level['limit'] - 2, gold_level['currentRemainingNumber'])

    def test_get_public_sponsors_입금_순으로_들어오는지_확인(self):
        sponsor_level = SponsorLevel.objects.get(name_ko='골드')
        Sponsor.objects.create(
            creator=self.user, level=sponsor_level, name='느린스폰서',
            accepted=True, submitted=True, paid_at=now())
        user2 = get_user_model().objects.create(
            username='user2',
            email='me@pycon.kr')
        past_dt = now() - timedelta(days=1)
        Sponsor.objects.create(
            creator=user2, level=sponsor_level, name='빠른스폰서',
            accepted=True, submitted=True, paid_at=past_dt)

        # When
        result = self.client.execute(SPONSORS)

        # Then
        sponsors = result.data['sponsors']
        self.assertEqual(sponsors[0]['name'], '빠른스폰서')
        self.assertEqual(sponsors[1]['name'], '느린스폰서')

    def test_get_public_sponsors_입금_순으로_들어오는지_확인_2(self):
        sponsor_level = SponsorLevel.objects.get(name_ko='골드')
        user2 = get_user_model().objects.create(
            username='user2',
            email='me@pycon.kr')
        past_dt = now() - timedelta(days=1)
        Sponsor.objects.create(
            creator=user2, level=sponsor_level, name='빠른스폰서',
            accepted=True, submitted=True, paid_at=past_dt)

        Sponsor.objects.create(
            creator=self.user, level=sponsor_level, name='느린스폰서',
            accepted=True, submitted=True, paid_at=now())

        sponsors = list(Sponsor.objects.all())
        # When
        result = self.client.execute(SPONSORS)

        # Then
        sponsors = result.data['sponsors']
        self.assertEqual(sponsors[0]['name'], '빠른스폰서')
        self.assertEqual(sponsors[1]['name'], '느린스폰서')

    def test_get_public_sponsor_조회_테스트(self):
        sponsor_level = SponsorLevel.objects.get(name_ko='골드')
        past_dt = now() - timedelta(days=1)
        sponsor = Sponsor.objects.create(
            creator=self.user, level=sponsor_level, name='스폰서',
            accepted=True, submitted=True, paid_at=past_dt)
        variables = {
            'id': to_global_id(PublicSponsorNode._meta.name, sponsor.pk)
        }

        # When
        result = self.client.execute(SPONSOR, variables=variables)

        # Then
        sponsor = result.data['sponsor']
        self.assertEqual(sponsor['name'], '스폰서')
