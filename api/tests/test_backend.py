from django.test import RequestFactory, testcases
from api.oauth_tokenbackend import OAuthTokenBackend


class UserTestCase(testcases.TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.backend = OAuthTokenBackend()

    def test_authenticate(self):
        request = self.request_factory.get('/')
        user = self.backend.authenticate(
            request=request, oauth_type='github', oauth_access_token='123')
        self.assertIsNotNone(user)
