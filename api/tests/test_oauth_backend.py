from unittest import skip
from django.test import RequestFactory, testcases
from api.oauth_tokenbackend import OAuthTokenBackend
from api.tests.data import initialize
from api.tests.common import generate_mock_response
from api.tests.oauth_app_response import \
    GITHUB_USER_RESPONSE,\
    GITHUB_EMAILS_RESPONSE, \
    GITHUB_ACCESS_TOKEN_RESPONSE


class OAuthTokenBackendTestCase(testcases.TestCase):
    def setUp(self):
        initialize()
        self.request_factory = RequestFactory()
        self.backend = OAuthTokenBackend()

    @skip
    def test_authenticate(self, mock_post, mock_get):
        # Given
        mock_access_token_resp = generate_mock_response(
            status=200, content=GITHUB_ACCESS_TOKEN_RESPONSE)
        mock_resp = generate_mock_response(
            status=200, json=GITHUB_USER_RESPONSE)
        mock_post.side_effect = [mock_access_token_resp]
        mock_get.side_effect = [mock_resp]
        request = self.request_factory.get('/')

        # When
        user = self.backend.authenticate(
            request=request, oauth_type='github',
            client_id='prod_github_client_id', code='TEST_CODE', redirect_uri='redirect_uri')

        # Then
        self.assertIsNotNone(user)
        self.assertEqual(
            f'prod_github_{GITHUB_USER_RESPONSE["id"]}', user.username)
        self.assertEqual(GITHUB_USER_RESPONSE['email'], user.email)
        self.assertEqual(
            GITHUB_USER_RESPONSE['avatar_url'], user.profile.avatar_url)
        self.assertEqual(GITHUB_USER_RESPONSE['login'], user.profile.name)

    @skip
    def test_authenticate_without_public_email(self, mock_post, mock_get):
        # Given
        dummy_user_response = GITHUB_USER_RESPONSE.copy()
        dummy_user_response['email'] = None
        mock_access_token_resp = generate_mock_response(
            status=200, content=GITHUB_ACCESS_TOKEN_RESPONSE)
        mock_user_resp = generate_mock_response(
            status=200, json=dummy_user_response)
        mock_email_resp = generate_mock_response(
            status=200, json=GITHUB_EMAILS_RESPONSE)

        mock_post.side_effect = [mock_access_token_resp]
        mock_get.side_effect = [
            mock_user_resp, mock_email_resp]
        request = self.request_factory.get('/')

        # When
        user = self.backend.authenticate(
            request=request, oauth_type='github',
            client_id='develop_github_client_id', code='TEST_CODE', redirect_uri='redirect_uri')

        # Then
        self.assertIsNotNone(user)
        self.assertEqual(
            f'develop_github_{GITHUB_USER_RESPONSE["id"]}', user.username)
        self.assertEqual(GITHUB_EMAILS_RESPONSE[0]['email'], user.email)
        self.assertEqual(GITHUB_USER_RESPONSE['login'], user.profile.name)
        self.assertEqual(
            GITHUB_USER_RESPONSE['avatar_url'], user.profile.avatar_url)
