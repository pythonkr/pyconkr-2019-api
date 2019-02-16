import json
from django.test import RequestFactory, testcases
from unittest import mock
from api.oauth_tokenbackend import OAuthTokenBackend, GITHUB_PROFILE_URL, GITHUB_EMAIL_URL


USER_RESPONSE = {
    "login": "amazingguni",
    "avatar_url": "https://avatars0.githubusercontent.com/u/13607839?v=4",
    "type": "User",
    "name": "amazingguni_test",
    "location": "Seoul, Korea",
    "email": "amazingguni@gmail.com",
    "bio": "Be a good engineer",
}


class OAuthTokenBackendTestCase(testcases.TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.backend = OAuthTokenBackend()

    @mock.patch('api.oauth_tokenbackend.requests.get')
    def test_authenticate(self, mock_get):
        # Given
        mock_resp = self._mock_response(
            status=200, json=USER_RESPONSE)

        mock_get.side_effect = [mock_resp]
        request = self.request_factory.get('/')

        # When
        user = self.backend.authenticate(
            request=request, oauth_type='github', oauth_access_token='TEST_TOKEN')

        # Then
        self.assertIsNotNone(user)
        self.assertEquals(f'github_{USER_RESPONSE["login"]}', user.username)
        self.assertEquals(USER_RESPONSE['email'], user.email)
        # self.assertEquals(USER_RESPONSE['avatar_url'], user.profile.avatar_url)

    def _mock_response(
            self,
            status=200,
            json={},
            raise_for_status=None):

        mock_resp = mock.Mock()

        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        mock_resp.json.return_value = json
        mock_resp.status_code = status
        mock_resp.content = str(json)

        return mock_resp
