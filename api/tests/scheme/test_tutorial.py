from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.models.program import Tutorial
from api.tests.base import BaseTestCase
from api.tests.scheme.tutorial_queries import TUTORIALS, TUTORIAL

TIMEZONE = get_current_timezone()

UserModel = get_user_model()


class TutorialTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)

    def test_get_tutorials(self):
        Tutorial.objects.create(name='튜토리얼', desc='설명', accepted=True)

        response = self.client.execute(TUTORIALS)
        data = response.data
        self.assertIsNotNone(data['tutorials'])
        self.assertIsNotNone(data['tutorials'][0])

    def test_get_presentation(self):
        tutorial = Tutorial.objects.create(name='튜토리얼', desc='설명', accepted=True)

        variables = {
            'id': tutorial.id
        }

        response = self.client.execute(TUTORIAL, variables)
        data = response.data
        self.assertIsNotNone(data['tutorial'])
        self.assertEqual(str(tutorial.id), str(data['tutorial']['id']))
