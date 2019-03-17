from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from graphql_jwt.testcases import JSONWebTokenTestCase
from api.tests.scheme.presentation_queries import CREATE_OR_UPDATE_PRESENTATION_PROPOSAL
TIMEZONE = get_current_timezone()

UserModel = get_user_model()


class PresentationTestCase(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)

    def test_create_or_update_proposal(self):
        variables = {
            'data': {
                'name': '흥미로운 GraphQL',
                'backgroundDesc': '자바',
                'detailDesc': 'GraphQL은 재미있다는 설명!',
                'language': 'KOREAN',
                'duration': 'SHORT',
                'isPresentedBefore': True,
                'placePresentedBefore': '학교 강당 앞',
                'presentedSlideUrlBefore': 'my.previous.url',
                'comment': '밥은 주시는거죠?',
                'submitted': True,
            }
        }

        expected = {
            'createOrUpdatePresentationProposal': {
                'proposal': {
                    **variables['data'],
                },
                'success': True
            }
        }

        response = self.client.execute(CREATE_OR_UPDATE_PRESENTATION_PROPOSAL, variables)
        self.assertDictEqual(response.data, expected)
