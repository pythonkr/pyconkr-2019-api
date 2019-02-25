from unittest import mock
from django.test import RequestFactory, testcases
from api.tests.base import BaseTestCase
from api.oauth_tokenbackend import OAuthTokenBackend
from api.tests.common import generate_mock_response
from api.tests.oauth_app_response import \
    GITHUB_USER_RESPONSE, GITHUB_EMAILS_RESPONSE,\
    GOOGLE_USER_RESPONSE, NAVER_USER_RESPONSE,\
    FACEBOOK_USER_RESPONSE


class OAuthTokenBackendTestCase(BaseTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.backend = OAuthTokenBackend()

    @mock.patch('api.oauth_tokenbackend.OAuth2Session.fetch_token')
    @mock.patch('api.oauth_tokenbackend.OAuth2Session.get')
    def test_github_authenticate(self, mock_get, mock_fetch_token):
        # Given
        mock_resp = generate_mock_response(
            status=200, json=GITHUB_USER_RESPONSE)
        mock_get.side_effect = [mock_resp]
        request = self.request_factory.get('/')

        # When
        user = self.backend.authenticate(
            request=request, oauth_type='github',
            client_id='prod_github_client_id',
            code='TEST_CODE', redirect_uri='REDIRECT_ME')

        # Then
        self.assertIsNotNone(user)
        self.assertEqual(
            f'prod_github_{GITHUB_USER_RESPONSE["id"]}', user.username)
        self.assertEqual(GITHUB_USER_RESPONSE['email'], user.email)
        self.assertEqual(
            GITHUB_USER_RESPONSE['avatar_url'], user.profile.avatar_url)
        self.assertEqual(GITHUB_USER_RESPONSE['login'], user.profile.name)

    @mock.patch('api.oauth_tokenbackend.OAuth2Session.fetch_token')
    @mock.patch('api.oauth_tokenbackend.OAuth2Session.get')
    def test_github_authenticate_without_public_email(self, mock_get, mock_fetch_token):
        # Given
        dummy_user_response = GITHUB_USER_RESPONSE.copy()
        dummy_user_response['email'] = None
        mock_user_resp = generate_mock_response(
            status=200, json=dummy_user_response)
        mock_email_resp = generate_mock_response(
            status=200, json=GITHUB_EMAILS_RESPONSE)
        mock_get.side_effect = [
            mock_user_resp, mock_email_resp]
        request = self.request_factory.get('/')

        # When
        user = self.backend.authenticate(
            request=request, oauth_type='github',
            client_id='develop_github_client_id',
            code='TEST_CODE', redirect_uri='REDIRECT_ME')

        # Then
        self.assertIsNotNone(user)
        self.assertEqual(
            f'develop_github_{GITHUB_USER_RESPONSE["id"]}', user.username)
        self.assertEqual(GITHUB_EMAILS_RESPONSE[0]['email'], user.email)
        self.assertEqual(GITHUB_USER_RESPONSE['login'], user.profile.name)
        self.assertEqual(
            GITHUB_USER_RESPONSE['avatar_url'], user.profile.avatar_url)


    @mock.patch('api.oauth_tokenbackend.OAuth2Session.fetch_token')
    @mock.patch('api.oauth_tokenbackend.OAuth2Session.get')
    def test_google_authenticate(self, mock_get, mock_fetch_token):
        # Given
        mock_resp = generate_mock_response(
            status=200, json=GOOGLE_USER_RESPONSE)
        mock_get.side_effect = [mock_resp]
        request = self.request_factory.get('/')

        # When
        user = self.backend.authenticate(
            request=request, oauth_type='google',
            client_id='prod_google_client_id',
            code='TEST_CODE', redirect_uri='REDIRECT_ME')

        # Then
        self.assertIsNotNone(user)
        self.assertEqual(
            f'prod_google_{GOOGLE_USER_RESPONSE["id"]}', user.username)
        self.assertEqual(GOOGLE_USER_RESPONSE['email'], user.email)
        self.assertEqual(
            GOOGLE_USER_RESPONSE['picture'], user.profile.avatar_url)
        self.assertEqual(GOOGLE_USER_RESPONSE['name'], user.profile.name)

    @mock.patch('api.oauth_tokenbackend.OAuth2Session.fetch_token')
    @mock.patch('api.oauth_tokenbackend.OAuth2Session.get')
    def test_facebook_authenticate(self, mock_get, mock_fetch_token):
        # Given
        mock_resp = generate_mock_response(
            status=200, json=FACEBOOK_USER_RESPONSE)
        mock_get.side_effect = [mock_resp]
        request = self.request_factory.get('/')

        # When
        user = self.backend.authenticate(
            request=request, oauth_type='facebook',
            client_id='prod_facebook_client_id',
            code='TEST_CODE', redirect_uri='REDIRECT_ME')

        # Then
        self.assertIsNotNone(user)
        self.assertEqual(
            f'prod_facebook_{FACEBOOK_USER_RESPONSE["id"]}', user.username)
        self.assertEqual(FACEBOOK_USER_RESPONSE['email'], user.email)
        self.assertEqual(
            FACEBOOK_USER_RESPONSE['picture']['data']['url'], user.profile.avatar_url)
        self.assertEqual(FACEBOOK_USER_RESPONSE['name'], user.profile.name)

    @mock.patch('api.oauth_tokenbackend.OAuth2Session.fetch_token')
    @mock.patch('api.oauth_tokenbackend.OAuth2Session.get')
    def test_naver_authenticate(self, mock_get, mock_fetch_token):
        # Given
        mock_resp = generate_mock_response(
            status=200, json=NAVER_USER_RESPONSE)
        mock_get.side_effect = [mock_resp]
        request = self.request_factory.get('/')

        # When
        user = self.backend.authenticate(
            request=request, oauth_type='naver',
            client_id='prod_naver_client_id',
            code='TEST_CODE', redirect_uri='REDIRECT_ME')

        # Then
        self.assertIsNotNone(user)
        self.assertEqual(
            f'prod_naver_{ NAVER_USER_RESPONSE["response"]["id"] }', user.username)
        self.assertEqual(NAVER_USER_RESPONSE['response']['email'], user.email)
        self.assertEqual(
            NAVER_USER_RESPONSE['response']['profile_image'], user.profile.avatar_url)
        self.assertEqual(NAVER_USER_RESPONSE['response']['name'], user.profile.name)
