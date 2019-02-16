from unittest import mock
from django.test import RequestFactory, testcases
from api.oauth_tokenbackend import OAuthTokenBackend


USER_RESPONSE = {
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
    def test_authenticate(self, mock_get):
        # Given
        mock_resp = self._mock_response(
            status=200, json=self.dummy_user_response)

        mock_get.side_effect = [mock_resp]
        request = self.request_factory.get('/')

        # When
        user = self.backend.authenticate(
            request=request, oauth_type='github', oauth_access_token='TEST_TOKEN')

        # Then
        self.assertIsNotNone(user)
        self.assertEqual(f'github_{USER_RESPONSE["login"]}', user.username)
        self.assertEqual(USER_RESPONSE['email'], user.email)
        self.assertEqual(USER_RESPONSE['login'], user.profile.name)
        self.assertEqual(USER_RESPONSE['avatar_url'], user.profile.avatar_url)

    @mock.patch('api.oauth_tokenbackend.requests.get')
    def test_authenticate_without_public_email(self, mock_get):
        # Given
        self.dummy_user_response['email'] = None
        mock_user_resp = self._mock_response(
            status=200, json=self.dummy_user_response)
        mock_email_resp = self._mock_response(
            status=200, json=self.dummy_emails_response)
        mock_get.side_effect = [mock_user_resp, mock_email_resp]
        request = self.request_factory.get('/')

        # When
        user = self.backend.authenticate(
            request=request, oauth_type='github', oauth_access_token='TEST_TOKEN')

        # Then
        self.assertIsNotNone(user)
        self.assertEqual(f'github_{USER_RESPONSE["login"]}', user.username)
        self.assertEqual(EMAILS_RESPONSE[0]['email'], user.email)
        self.assertEqual(USER_RESPONSE['login'], user.profile.name)
        self.assertEqual(USER_RESPONSE['avatar_url'], user.profile.avatar_url)

    def _mock_response(
            self,
            status=200,
            json=None,
            raise_for_status=None):

        mock_resp = mock.Mock()

        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        mock_resp.json.return_value = json
        mock_resp.status_code = status
        mock_resp.content = str(json)

        return mock_resp
