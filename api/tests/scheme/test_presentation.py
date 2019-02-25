from json import loads, dumps
from datetime import datetime
from django.utils.timezone import get_current_timezone
from django.contrib.auth import get_user_model
from api.tests.base import BaseTestCase
from api.schema import schema
from api.tests.common import generate_request_authenticated, \
    generate_request_anonymous
TIMEZONE = get_current_timezone()

UserModel = get_user_model()

PRESENTATION_QUERY = '''
query {
    presentations {
        name
        nameKo
        nameEn
        desc
        descKo
        descEn
        price
        visible
        language
        owner {
            username
        }
        accepted
        place {
            name
        }
        startedAt
        finishedAt
        category {
            name
            nameKo
            nameEn
            slug
            visible
        }
        slideUrl
        pdfUrl
        videoUrl
        difficulty {
            name
            nameKo
            nameEn
        }
        recordable
    }
}
'''


class PresentationTestCase(BaseTestCase):
    def test_create_presentation(self):
        mutation = '''
        mutation CreatePresentation($presentationInput: PresentationInput!,
                $categoryId: Int, $difficultyId: Int) {
            createPresentation(presentationInput: $presentationInput, categoryId: $categoryId, difficultyId: $difficultyId) {
                presentation {
                    id
                    nameKo
                    nameEn
                    descKo
                    descEn
                    language
                    submitted
                    slideUrl
                    pdfUrl
                    videoUrl
                    recordable
                    category {
                        id
                    }
                    difficulty {
                        id
                    }
                }
            }
        }
        '''

        variables = {
            'categoryId': 1,
            'difficultyId': 1,
            'presentationInput': {
                'nameKo': '흥미로운 GraphQL',
                'nameEn': 'Interesting GraphQL',
                'descKo': 'GraphQL은 재미있다는 설명!',
                'descEn': 'The description that GraphQL is fun',
                'language': 'KOREAN',
                'submitted': True,
                'slideUrl': 'my.slide.url',
                'pdfUrl': 'my.pdf.url',
                'videoUrl': 'my.video.url',
                'recordable': True
            }
        }

        expected = {
            'createPresentation': {
                'presentation': {
                    **variables['presentationInput'],
                    'category': {
                        'id': '1'
                    },
                    'difficulty': {
                        'id': '1'
                    }
                }
            }
        }
        user = UserModel(username='develop_github_123', email='me@pycon.kr')
        user.save()
        request = generate_request_authenticated(user)

        # When
        result = schema.execute(
            mutation, variables=variables, context_value=request)

        # Then
        actual = loads(dumps(result.data))
        self.assertIsNotNone(actual)
        self.assertIsNotNone(
            actual['createPresentation']['presentation']['id'])
        del actual['createPresentation']['presentation']['id']
        self.assertDictEqual(actual, expected)

    def test_create_presentation_only_name(self):
        mutation = '''
        mutation CreatePresentation($presentationInput: PresentationInput!,
                $categoryId: Int, $difficultyId: Int) {
            createPresentation(presentationInput: $presentationInput, categoryId: $categoryId, difficultyId: $difficultyId) {
                presentation {
                    id
                    nameKo
                    nameEn
                }
            }
        }
        '''

        variables = {
            'presentationInput': {
                'nameKo': '흥미로운 GraphQL',
                'nameEn': 'Interesting GraphQL',
            }
        }

        expected = {
            'createPresentation': {
                'presentation': {
                    **variables['presentationInput'],
                }
            }
        }
        user = UserModel(username='develop_github_123', email='me@pycon.kr')
        user.save()
        request = generate_request_authenticated(user)

        # When
        result = schema.execute(
            mutation, variables=variables, context_value=request)

        # Then
        actual = loads(dumps(result.data))
        self.assertIsNotNone(actual)
        self.assertIsNotNone(
            actual['createPresentation']['presentation']['id'])
        del actual['createPresentation']['presentation']['id']
        self.assertDictEqual(actual, expected)

    def test_retrieve_presentation(self):
        # Given
        expected = {
            'name': '작성중인 발표',
            'nameKo': '작성중인 발표',
            'nameEn': 'Before submitting',
            'desc': '작성중인 발표입니다.',
            'descKo': '작성중인 발표입니다.',
            'descEn': 'It is onprogress presentation',
            'price': 0,
            'visible': False,
            'language': 'KOREAN',
            'owner': {
                'username': 'testuser'
            },
            'accepted': False,
            'place': {
                'name': '101'
            },
            'startedAt': datetime(2019, 8, 21, 13, 00).astimezone(tz=TIMEZONE).isoformat(),
            'finishedAt': datetime(2019, 8, 21, 15, 00).astimezone(tz=TIMEZONE).isoformat(),
            'category': {
                'name': 'Web Service',
                'nameKo': 'Web Service',
                'nameEn': 'Web Service',
                'slug': 'web_service',
                'visible': True
            },
            'slideUrl': 'https://slide/1',
            'pdfUrl': 'https://pdf/1',
            'videoUrl': 'https://video/1',
            'difficulty': {
                'name': '초급',
                'nameKo': '초급',
                'nameEn': 'Beginner'
            },
            'recordable': True
        }

        user = UserModel.objects.get(username='testuser')
        request = generate_request_authenticated(user)

        # When
        result = schema.execute(PRESENTATION_QUERY, context_value=request)

        # Then
        actual = loads(dumps(result.data))
        self.assertIn('presentations', actual)
        self.assertDictEqual(actual['presentations'][0], expected)

    def test_should_not_retrieve_unaccepted_presentation_to_anonymous(self):
        request = generate_request_anonymous()

        # When
        result = schema.execute(PRESENTATION_QUERY, context_value=request)

        # Then
        actual = loads(dumps(result.data))
        self.assertEqual(1, len(actual['presentations']))

    def test_retrieve_unaccepted_presentation_to_only_owner(self):
        user = UserModel.objects.create(username='other_user')
        user.save()
        request = generate_request_authenticated(user)

        # When
        result = schema.execute(PRESENTATION_QUERY, context_value=request)

        # Then
        actual = loads(dumps(result.data))
        self.assertEqual(1, len(actual['presentations']))
