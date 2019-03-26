from datetime import datetime
from json import loads, dumps

from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from api.tests.base import BaseTestCase
from api.schema import schema
from api.tests.common import generate_request_authenticated

TIMEZONE = get_current_timezone()

UserModel = get_user_model()

SPONSOR_QUERY = '''
query {
   sponsors {
        nameKo
        nameEn
        descKo
        descEn
        url
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
        mutation CreateOrUpdateSponsor($SponsorInput: SponsorInput!) {
            createOrUpdateSponsor(sponsorInput: $sponsorInput) {
                sponsor {
                    id
                    name
                    nameKo
                    nameEn
                    descKo
                    descEn
                    url
                    level
                    paidAt
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
                'url': 'my.slide.url',
                'level': '6',
                'paidAt': '2019-03-20'
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
        query = SPONSOR_QUERY

        expected = {
            'nameKo': '파이콘한국',
            'nameEn': 'Pycon Korea',
            'descKo': '파이콘 한국입니다',
            'descEn': 'we are pycon korea',
            'url': 'http://pythonkr/1',
            'level': {
                'name': '키스톤',
                'price': 20000000,
                'ticketCount': 20
            },
            'paidAt': datetime(2019, 8, 21, 13, 00).astimezone(tz=TIMEZONE).isoformat(),
        }

        # When
        result = schema.execute(query)

        # Then
        actual = loads(dumps(result.data))
        self.assertIn('sponsors', actual)
        self.assertDictEqual(actual['sponsors'][0], expected)
