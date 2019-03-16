from json import loads, dumps
import unittest
from django.utils.timezone import get_current_timezone
from django.contrib.auth import get_user_model

from graphql_extensions.testcases import SchemaTestCase
from api.tests.common import generate_request_authenticated

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
mutation createOrUpdatePresentationProposal($input: PresentationProposalInput!) {
    createOrUpdatePresentationProposal(input: $input) {
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


class PresentationTestCase(SchemaTestCase):
    @unittest.skip('TODO 로그인 처리 후 살릴 예정')
    def test_create_proposal(self):
        variables = {
            'input': {
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
                    **variables['input'],
                },
                'success': True
            }
        }
        user = UserModel(username='develop_github_123', email='me@pycon.kr')
        user.save()
        request = generate_request_authenticated(user)
        self.client.force_login(user)

        # When
        result = self.client.execute(
            PROPOSAL_UPDATE_MUTATION, variables=variables, context_value=request)

        # Then
        actual = loads(dumps(result.data))
        self.assertIsNotNone(actual)
        self.assertDictEqual(actual, expected)
