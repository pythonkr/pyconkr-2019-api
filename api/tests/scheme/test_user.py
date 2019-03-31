from json import loads, dumps
from unittest import mock

from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from graphql_extensions.exceptions import PermissionDenied
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.tests.base import BaseTestCase
from api.tests.common import generate_mock_response
from api.tests.oauth_app_response import GITHUB_USER_RESPONSE
from api.tests.scheme.user_queries import ME, UPDATE_PROFILE, UPDATE_AGREEMENT

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
