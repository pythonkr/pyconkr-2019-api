from datetime import datetime
from json import loads, dumps

from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from api.tests.base import BaseTestCase
from api.schema import schema
from api.tests.common import generate_request_authenticated, generate_request_anonymous

TIMEZONE = get_current_timezone()

UserModel = get_user_model()

SPONSOR_QUERY = '''
query {
   sponsors {
        name
        nameKo
        nameEn
        desc
        descKo
        descEn
        url
        owner {
            username
        }
        level {
            name
            price
            ticketCount
        }
        paidAt
    }
}
'''


class SponsorTestCase(BaseTestCase):
    def test_create_sponsor(self):
        mutation = '''
        mutation CreateOrUpdateSponsor($sponsorInput: SponsorInput!) {
            createOrUpdateSponsor(sponsorInput: $sponsorInput) {
                sponsor {
                    id
                    name
                    nameKo
                    nameEn
                    descKo
                    descEn
                    url
                }
            }
        }
        '''

        variables = {
            'sponsorInput': {
                'name': '안 흥미로운 GraphQL',
                'nameKo': '안 흥미로운 GraphQL',
                'nameEn': 'Not Interesting GraphQL',
                'descKo': 'GraphQL은 재미있다는 설명은함정!',
                'descEn': 'The description that GraphQL is Trap!',
                'url': 'my.slide.url'
            }
        }

        expected = {
            'createOrUpdateSponsor': {
                'sponsor': {
                    **variables['sponsorInput'],
                }
            }
        }
        user = UserModel(username='develop_github_123', email='me@pycon.kr')
        user.save()
        request = generate_request_authenticated(user)

        # When
        result = schema.execute(
            mutation, variables=variables, context_value=request)

        # Then
        actual = loads(dumps(result.data))
        self.assertIsNotNone(actual)
        self.assertIsNotNone(
            actual['createOrUpdateSponsor']['sponsor']['id'])
        del actual['createOrUpdateSponsor']['sponsor']['id']
        self.assertDictEqual(actual, expected)

    def test_create_sponsor_only_name(self):
        mutation = '''
        mutation CreateOrUpdateSponsor($sponsorInput: SponsorInput!) {
            createOrUpdateSponsor(sponsorInput: $sponsorInput) {
                sponsor {
                    id
                    name
                    nameKo
                    nameEn
                }
            }
        }
        '''

        variables = {
            'sponsorInput': {
                'name': '흥미로운 GraphQL',
                'nameKo': '흥미로운 GraphQL',
                'nameEn': 'Interesting GraphQL',
            }
        }

        expected = {
            'createOrUpdateSponsor': {
                'sponsor': {
                    **variables['sponsorInput'],
                }
            }
        }

        user = UserModel(username='develop_github_123', email='me@pycon.kr')
        user.save()
        request = generate_request_authenticated(user)

        # When
        result = schema.execute(
            mutation, variables=variables, context_value=request)

        # Then
        actual = loads(dumps(result.data))
        self.assertIsNotNone(actual)
        self.assertIsNotNone(
            actual['createOrUpdateSponsor']['sponsor']['id'])
        del actual['createOrUpdateSponsor']['sponsor']['id']
        self.assertDictEqual(actual, expected)

    def test_retrieve_sponsor(self):
        # Given
        expected = {
            'name': '입금전후원사',
            'nameKo': '입금전후원사',
            'nameEn': 'NotPaid',
            'desc': '아직 입금하지 않은 후원사입니다',
            'descKo': '아직 입금하지 않은 후원사입니다',
            'descEn': 'We have not paid yet',
            'url': 'http://unpaid.com',
            'owner': {
                'username': 'testuser'
            },
            'level': {
                'name': '미입금',
                'price': 0,
                'ticketCount': 0
            },
            'paidAt': datetime(2019, 8, 21, 13, 00).astimezone(tz=TIMEZONE).isoformat(),
        }

        user = UserModel.objects.get(username='testuser')
        request = generate_request_authenticated(user)

        # When
        result = schema.execute(SPONSOR_QUERY, context_value=request)

        # Then
        actual = loads(dumps(result.data))
        self.assertIn('sponsors', actual)
        self.assertDictEqual(actual['sponsors'][0], expected)
