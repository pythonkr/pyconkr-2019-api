from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from graphql_jwt.testcases import JSONWebTokenTestCase

TIMEZONE = get_current_timezone()

UserModel = get_user_model()

MY_PROPOSAL_QUERY = '''
query {
    myPresentationProposal {
        name
        owner {
            username
        }
        backgroundDesc
        detailDesc
        language
        duration
        category {
            name
            nameKo
            nameEn
            slug
            visible
        }
        difficulty {
            name
            nameKo
            nameEn
        }
        isPresentedBefore
        placePresentedBefore
        presentedSlideUrlBefore
        comment
        isAgreed
        recordable
        submitted
        accepted
    }
}
'''

PROPOSAL_UPDATE_MUTATION = '''
mutation createOrUpdatePresentationProposal($data: PresentationProposalInput!) {
    createOrUpdatePresentationProposal(data: $data) {
        proposal {
          name
          backgroundDesc
          detailDesc
          language
          duration
          isPresentedBefore
          placePresentedBefore
          presentedSlideUrlBefore
          comment
          submitted
        }
        success
    }
}
'''


class PresentationTestCase(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)

    def test_create_user(self):
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

        response = self.client.execute(PROPOSAL_UPDATE_MUTATION, variables)
        self.assertDictEqual(response.data, expected)
