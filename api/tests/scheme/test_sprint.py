from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.models.program import Sprint
from api.tests.base import BaseTestCase
from api.tests.scheme.sprint_queries import SPRINT, SPRINTS

TIMEZONE = get_current_timezone()

UserModel = get_user_model()


class SprintTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)

    def test_get_sprints(self):
        Sprint.objects.create(name='스프린트', desc='설명', accepted=True)

        response = self.client.execute(SPRINTS)
        data = response.data
        self.assertIsNotNone(data['sprints'])
        self.assertIsNotNone(data['sprints'][0])

    def test_get_sprint(self):
        sprint = Sprint.objects.create(name='스프린트', desc='설명', accepted=True)

        variables = {
            'id': sprint.id
        }

        response = self.client.execute(SPRINT, variables)
        data = response.data
        self.assertIsNotNone(data['sprint'])
        self.assertEqual(str(sprint.id), str(data['sprint']['id']))
