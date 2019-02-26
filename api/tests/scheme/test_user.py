from unittest import mock
from json import loads, dumps
from django.utils.timezone import get_current_timezone
from django.contrib.auth import get_user_model
from api.tests.base import BaseTestCase
from api.schema import schema

from api.tests.common import \
    generate_mock_response, \
    generate_request_authenticated, \
    generate_request_anonymous

from api.tests.oauth_app_response import GITHUB_USER_RESPONSE


TIMEZONE = get_current_timezone()
UserModel = get_user_model()

PROFILE_QUERY = '''
query {
    me {
        username
        email
        profile {
            name
            bio
            phone
            organization
            nationality
        }
    }
}
'''

class UserTestCase(BaseTestCase):
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
        result = schema.execute(mutation, variables=variables)

        # Then
        actual = loads(dumps(result.data))
        self.assertIsNotNone(actual['oAuthTokenAuth']['token'])

    def test_update_profile(self):
        # Given
        mutation = '''
        mutation UpdateProfile($profileInput: ProfileInput!) {
            updateProfile(profileInput: $profileInput) {
                profile {
                    user {
                        username
                        email
                    }
                    name
                    bio
                    phone
                    organization
                    nationality
                }
            }
        }
        '''
        variables = {
            'profileInput': {
                'name': '코니',
                'bio': '파이콘 한국을 참석하고 있지요',
                'phone': '010-1111-1111',
                'organization': '파이콘!',
                'nationality': '미국',
            }
        }

        expected = {
            'updateProfile': {
                'profile': {
                    'user': {
                        'username': 'develop_github_123',
                        'email': 'me@pycon.kr'
                    },
                    **variables['profileInput']
                }
            }
        }

        user = UserModel(username='develop_github_123', email='me@pycon.kr')
        user.save()
        request = generate_request_authenticated(user)
        result = schema.execute(
            mutation, variables=variables, context_value=request)

        # Then
        actual = loads(dumps(result.data))
        self.assertIsNotNone(actual)
        self.assertDictEqual(actual, expected)

    def test_me(self):
        # Given
        user = UserModel(username='develop_github_123', email='me@pycon.kr')
        user.save()
        user.profile.name = 'pycon_angel'
        user.profile.bio = '파이콘 천사입니다.'
        user.profile.phone = '222-2222-2222'
        user.profile.organization = '좋은회사'
        user.profile.nationality = '우리나라'
        user.save()

        request = generate_request_authenticated(user)

        # When
        result = schema.execute(PROFILE_QUERY, context_value=request)
        expected = {
            'me': {
                'username': 'develop_github_123',
                'email': 'me@pycon.kr',
                'profile': {
                    'name': 'pycon_angel',
                    'bio': '파이콘 천사입니다.',
                    'phone': '222-2222-2222',
                    'organization': '좋은회사',
                    'nationality': '우리나라'
                }
            }
        }

        # Then
        actual = loads(dumps(result.data))
        self.assertIsNotNone(actual)
        self.assertDictEqual(actual, expected)

    def test_me_anonymous(self):
        request = generate_request_anonymous()
        # When
        result = schema.execute(PROFILE_QUERY, context_value=request)
        self.assertIsNotNone(result.errors)
