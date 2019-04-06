# from datetime import datetime
# from json import loads, dumps
#
# from django.contrib.auth import get_user_model
# from django.utils.timezone import get_current_timezone
# from api.tests.base import BaseTestCase
# from api.schema import schema
# from api.tests.common import generate_request_authenticated
#
# TIMEZONE = get_current_timezone()
#
# UserModel = get_user_model()
# SPONSOR_QUERY = '''
# query {
#    sponsors {
#         creator {
#             username
#         }
#         name
#         nameKo
#         nameEn
#         manager_name
#         manager_phone
#         manager_secondary_phone
#         manager_email
#         level {
#             name
#             price
#             ticketCount
#         }
#         business_registration_number
#         contact_process_required
#         url
#         desc
#         descKo
#         descEn
#         paidAt
#         accepted
#     }
# }
# '''
#
#
# class SponsorTestCase(BaseTestCase):

from django.test import RequestFactory
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from api.tests.base import BaseTestCase
from api.tests.scheme.sponsor_queries import CREATE_OR_UPDATE_SPONSER


class SponsorTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)
        self.factory = RequestFactory()

    def test_create_or_update_sponsor(self):
        variables = {
            'sponsorInput': {
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
                'contract_process_required': True,
                'url': 'my.slide.url'
            }
        }

        # When
        result = self.client.execute(CREATE_OR_UPDATE_SPONSER, variables=variables)
        result

#
#     def test_create_sponsor_only_name(self):
#         mutation = '''
#         mutation CreateOrUpdateSponsor($sponsorInput: SponsorInput!) {
#             createOrUpdateSponsor(sponsorInput: $sponsorInput) {
#                 sponsor {
#                     id
#                     name
#                     nameKo
#                     nameEn
#                 }
#             }
#         }
#         '''
#
#         variables = {
#             'sponsorInput': {
#                 'name': '흥미로운 GraphQL',
#                 'nameKo': '흥미로운 GraphQL',
#                 'nameEn': 'Interesting GraphQL',
#             }
#         }
#
#         expected = {
#             'createOrUpdateSponsor': {
#                 'sponsor': {
#                     **variables['sponsorInput'],
#                 }
#             }
#         }
#
#         user = UserModel(username='develop_github_123', email='me@pycon.kr')
#         user.save()
#         request = generate_request_authenticated(user)
#
#         # When
#         result = schema.execute(
#             mutation, variables=variables, context_value=request)
#
#         # Then
#         actual = loads(dumps(result.data))
#         self.assertIsNotNone(actual)
#         self.assertIsNotNone(
#             actual['createOrUpdateSponsor']['sponsor']['id'])
#         del actual['createOrUpdateSponsor']['sponsor']['id']
#         self.assertDictEqual(actual, expected)
#
#
#     def test_retrieve_sponsor(self):
#         # Given
#         expected = {
#             'creator': {
#                 'username': 'testuser'
#             },
#             'name': '입금전후원사',
#             'nameKo': '입금전후원사',
#             'nameEn': 'NotPaid',
#             'manager_name': '이현호',
#             'manager_phone': '01040555880',
#             'manager_secondary_phone': '01072705880',
#             'manager_email': 'mizzking75@gmail.com',
#             'level': {
#                 'name': '미입금',
#                 'price': 0,
#                 'ticketCount': 0
#             },
#             'business_registration_number': '1002302-01',
#             'contact_process_required': False,
#             'url': 'http://unpaid.com',
#             'desc': '아직 입금하지 않은 후원사입니다',
#             'descKo': '아직 입금하지 않은 후원사입니다',
#             'descEn': 'We have not paid yet',
#             'paidAt': datetime(2019, 8, 21, 13, 00).astimezone(tz=TIMEZONE).isoformat(),
#             'accepted': datetime(2019, 8, 21, 13, 00).astimezone(tz=TIMEZONE).isoformat(),
#         }
#
#         creator = UserModel.objects.get(username='testuser')
#         request = generate_request_authenticated(creator)
#
#         # When
#         result = schema.execute(SPONSOR_QUERY, context_value=request)
#
#         # Then
#         actual = loads(dumps(result.data))
#         self.assertIn('sponsors', actual)
#         self.assertDictEqual(actual['sponsors'][0], expected)