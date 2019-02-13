from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase


class UsersTests(JSONWebTokenTestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    def test_get_user(self):
        query = '''
        query GetUser($username: String!) {
          user(username: $username) {
            id
          }
        }'''

        variables = {
            'username': self.user.username,
        }

        self.client.execute(query, variables=variables)
