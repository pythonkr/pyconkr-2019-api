from unittest import mock
from django.test import RequestFactory, testcases
from api.oauth_tokenbackend import OAuthTokenBackend

ACCESS_TOKEN_RESPONSE = b'access_token=111767d60d69f06812b54ca7b5bb46c49358a4ec&token_type=bearer'

USER_RESPONSE = {
    "id": 14,
    "login": "amazingguni",
    "avatar_url": "https://avatars0.githubusercontent.com/u/13607839?v=4",
    "type": "User",
    "name": "amazingguni_test",
    "location": "Seoul, Korea",
    "email": "amazingguni@gmail.com",
    "bio": "Be a good engineer",
}

EMAILS_RESPONSE = [
    {
        "email": "amazingguni@pycon.kr",
        "primary": True,
        "verified": True,
        "visibility": "public"
    }
]


class OAuthTokenBackendTestCase(testcases.TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.backend = OAuthTokenBackend()
        self.dummy_user_response = USER_RESPONSE.copy()
        self.dummy_emails_response = EMAILS_RESPONSE.copy()

    @mock.patch('api.oauth_tokenbackend.requests.get')
    @mock.patch('api.oauth_tokenbackend.requests.post')
    def test_authenticate(self, mock_post, mock_get):
        # Given
        mock_access_token_resp = self._mock_response(
            status=200, content=ACCESS_TOKEN_RESPONSE)
        mock_resp = self._mock_response(
            status=200, json=self.dummy_user_response)
        mock_post.side_effect = [mock_access_token_resp]
        mock_get.side_effect = [mock_resp]
        request = self.request_factory.get('/')

        # When
        user = self.backend.authenticate(
            request=request, oauth_type='github', code='TEST_CODE')

        # Then
        self.assertIsNotNone(user)
        self.assertEqual(f'github_{USER_RESPONSE["id"]}', user.username)
        self.assertEqual(USER_RESPONSE['email'], user.email)
        self.assertEqual(USER_RESPONSE['avatar_url'], user.profile.avatar_url)
        self.assertEqual(USER_RESPONSE['login'], user.profile.name)

    @mock.patch('api.oauth_tokenbackend.requests.get')
    @mock.patch('api.oauth_tokenbackend.requests.post')
    def test_authenticate_without_public_email(self, mock_post, mock_get):
        # Given
        self.dummy_user_response['email'] = None
        mock_access_token_resp = self._mock_response(
            status=200, content=ACCESS_TOKEN_RESPONSE)
        mock_user_resp = self._mock_response(
            status=200, json=self.dummy_user_response)
        mock_email_resp = self._mock_response(
            status=200, json=self.dummy_emails_response)

        mock_post.side_effect = [mock_access_token_resp]
        mock_get.side_effect = [
            mock_user_resp, mock_email_resp]
        request = self.request_factory.get('/')

        # When
        user = self.backend.authenticate(
            request=request, oauth_type='github', code='TEST_TOKEN')

        # Then
        self.assertIsNotNone(user)
        self.assertEqual(f'github_{USER_RESPONSE["id"]}', user.username)
        self.assertEqual(EMAILS_RESPONSE[0]['email'], user.email)
        self.assertEqual(USER_RESPONSE['login'], user.profile.name)
        self.assertEqual(USER_RESPONSE['avatar_url'], user.profile.avatar_url)

    def _mock_response(
            self,
            status=200,
            content='',
            json=None,
            raise_for_status=None):

        mock_resp = mock.Mock()

        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        mock_resp.json.return_value = json
        mock_resp.status_code = status
        if json:
            mock_resp.content = str(json)
        else:
            mock_resp.content = content

        return mock_resp
