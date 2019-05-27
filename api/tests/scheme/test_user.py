from datetime import timedelta
from json import loads, dumps
from unittest import mock

from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from django.utils.timezone import now
from graphql_extensions.exceptions import PermissionDenied
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.tests.base import BaseTestCase
from api.tests.common import generate_mock_response
from api.tests.oauth_app_response import GITHUB_USER_RESPONSE
from api.tests.scheme.user_queries import ME, UPDATE_PROFILE, UPDATE_AGREEMENT, PATRONS
from ticket.models import TicketProduct, Ticket

TIMEZONE = get_current_timezone()
UserModel = get_user_model()


class UserTestCase(BaseTestCase, JSONWebTokenTestCase):
    @mock.patch('api.oauth_tokenbackend.OAuth2Session.fetch_token')
    @mock.patch('api.oauth_tokenbackend.OAuth2Session.get')
    def test_oauth_token_auth(self, mock_get, mock_fetch_token):
        # Given
        mock_resp = generate_mock_response(
            status=200, json=GITHUB_USER_RESPONSE)
        mock_get.side_effect = [mock_resp]

        # Given
        mutation = '''
        mutation OAuthTokenAuth($oauthType: String!, $clientId: String!, $code: String!, $redirectUri: String!) {
            oAuthTokenAuth(oauthType: $oauthType, clientId: $clientId, code: $code, redirectUri: $redirectUri) {
                token
            }
        }
        '''
        variables = {
            'oauthType': 'github',
            'clientId': 'prod_github_client_id',
            'code': 'CODE',
            'redirectUri': 'REDIRECT_ME'
        }

        # When
        result = self.client.execute(mutation, variables)

        # Then
        actual = loads(dumps(result.data))
        self.assertIsNotNone(actual['oAuthTokenAuth']['token'])

    def test_update_profile(self):
        # Given

        variables = {
            'data': {
                'nameKo': '코니',
                'nameEn': 'Coni',
                'bioKo': '파이콘 한국을 참석하고 있지요',
                'bioEn': 'PyCon Korea Good',
                'phone': '010-1111-1111',
                'email': 'pyconkr@pycon.kr',
                'organization': '파이콘!',
                'nationality': '미국',
            }
        }
        user = UserModel(username='develop_github_123', email='me@pycon.kr')
        user.save()
        self.client.authenticate(user)
        result = self.client.execute(
            UPDATE_PROFILE, variables)

        # Then
        actual = loads(dumps(result.data))
        self.assertIsNotNone(actual)
        profile = actual['updateProfile']['profile']
        self.assertEqual(profile['nameKo'], '코니')
        self.assertEqual(profile['nameEn'], 'Coni')
        self.assertEqual(profile['bioKo'], '파이콘 한국을 참석하고 있지요')
        self.assertEqual(profile['bioEn'], 'PyCon Korea Good')
        self.assertEqual(profile['phone'], '010-1111-1111')
        self.assertEqual(profile['email'], 'pyconkr@pycon.kr')
        self.assertEqual(profile['organization'], '파이콘!')
        self.assertEqual(profile['nationality'], '미국')

    def test_me(self):
        # Given
        user = UserModel(username='develop_github_123')
        user.save()
        user.profile.name_ko = '파이콘 천사'
        user.profile.name_en = 'pycon_angel'
        user.profile.bio_ko = '파이콘 천사입니다.'
        user.profile.bio_en = "I'm pycon angel."
        user.profile.email = 'me@pycon.kr'
        user.profile.phone = '222-2222-2222'
        user.profile.organization = '좋은회사'
        user.profile.nationality = '우리나라'
        user.save()

        self.client.authenticate(user)

        # When
        result = self.client.execute(ME)

        # Then
        actual = loads(dumps(result.data))
        self.assertIsNotNone(actual)
        profile = actual['me']['profile']
        self.assertEqual(profile['nameKo'], '파이콘 천사')
        self.assertEqual(profile['nameEn'], 'pycon_angel')
        self.assertEqual(profile['bioKo'], '파이콘 천사입니다.')
        self.assertEqual(profile['bioEn'], 'I\'m pycon angel.')
        self.assertEqual(profile['email'], 'me@pycon.kr')
        self.assertEqual(profile['phone'], '222-2222-2222')
        self.assertEqual(profile['organization'], '좋은회사')
        self.assertEqual(profile['nationality'], '우리나라')

    def test_me_anonymous(self):
        # When
        actual = self.client.execute(ME)
        self.assertIsNotNone(actual.errors)
        self.assertIsInstance(actual.errors[0].original_error, PermissionDenied)

    def test_agreed_all(self):
        # Given
        user = UserModel.objects.create(username='develop_github_123')
        self.client.authenticate(user)
        variable = {
            'isPrivacyPolicy': True,
            'isTermsOfService': True,
        }

        result = self.client.execute(UPDATE_AGREEMENT, variable)
        self.assertIsNotNone(result.data['updateAgreement'])
        self.assertTrue(result.data['updateAgreement']['isAgreedAll'])

    def test_WHEN_동의를_다_하지_않으면_THEN_is_agreed_all이_False_여야한다(self):
        # Given
        user = UserModel.objects.create(username='develop_github_123')
        self.client.authenticate(user)
        variable = {
            'isPrivacyPolicy': False,
            'isTermsOfService': True,
        }

        result = self.client.execute(UPDATE_AGREEMENT, variable)
        self.assertIsNotNone(result.data['updateAgreement'])
        self.assertFalse(result.data['updateAgreement']['isAgreedAll'])

    def test_WHEN_최초에는_THEN_is_agreed_all이_False_여야한다(self):
        # Given
        user = UserModel.objects.create(username='develop_github_123')
        self.assertFalse(user.agreement.is_agreed_all())

    def test_patrons_without_patron_product_THEN_error(self):
        result = self.client.execute(PATRONS)
        self.assertIsNotNone(result.errors)

    def test_patrons(self):
        user1 = get_user_model().objects.create(
            username='user1',
            email='me@pycon.kr')
        user1.profile.name = 'user1'
        user1.save()
        user2 = get_user_model().objects.create(
            username='user2',
            email='me@pycon.kr')
        user2.profile.name = 'user2'
        user2.save()
        user3 = get_user_model().objects.create(
            username='user3',
            email='me@pycon.kr')
        user3.profile.name = 'user3'
        user3.save()
        user4 = get_user_model().objects.create(
            username='user4',
            email='me@pycon.kr')
        user4.profile.name = 'user4'
        user4.save()
        user5 = get_user_model().objects.create(
            username='user5',
            email='me@pycon.kr')
        user5.profile.name = 'user5'
        user5.save()
        user6 = get_user_model().objects.create(
            username='user6',
            email='me@pycon.kr')
        user6.profile.name = 'user6'
        user6.save()

        product = TicketProduct.objects.create(name='Patron', type=TicketProduct.TYPE_CONFERENCE,
                                               is_editable_price=True, active=True)
        Ticket.objects.create(owner=user1, product=product, status=Ticket.STATUS_PAID, amount=3000, paid_at=now())
        Ticket.objects.create(owner=user2, product=product, status=Ticket.STATUS_PAID, amount=2000, paid_at=now())
        Ticket.objects.create(
            owner=user3, product=product, status=Ticket.STATUS_PAID, amount=4000, paid_at=now() - timedelta(days=2))
        Ticket.objects.create(
            owner=user4, product=product, status=Ticket.STATUS_PAID, amount=4000, paid_at=now() - timedelta(days=3))
        Ticket.objects.create(
            owner=user5, product=product, status=Ticket.STATUS_PAID, amount=4000, paid_at=now())
        Ticket.objects.create(
            owner=user6, product=product, status=Ticket.STATUS_CANCELLED, amount=4000, paid_at=now())
        result = self.client.execute(PATRONS)
        self.assertIsNone(result.errors)
        self.assertIsNotNone(result.data['patrons'])
        self.assertEqual(5, len(result.data['patrons']))
        self.assertEqual('user4', result.data['patrons'][0]['name'])
        self.assertEqual('user3', result.data['patrons'][1]['name'])
        self.assertEqual('user5', result.data['patrons'][2]['name'])
        self.assertEqual('user1', result.data['patrons'][3]['name'])
        self.assertEqual('user2', result.data['patrons'][4]['name'])
