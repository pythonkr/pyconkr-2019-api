from json import loads, dumps
from datetime import datetime
from django.utils.timezone import get_current_timezone
from django.contrib.auth import get_user_model
from api.tests.base import BaseTestCase
from api.tests.data import initialize
from api.schema import schema
from api.tests.common import generate_request_authenticated
TIMEZONE = get_current_timezone()

UserModel = get_user_model()


class PresentationTestCase(BaseTestCase):
    def setUp(self):
        initialize()

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
        query = '''
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

        expected = {
            'presentations': [
                {
                    'name': 'Graphql로 api를 만들어보자',
                    'nameKo': 'Graphql로 api를 만들어보자',
                    'nameEn': 'Make api using Graphql',
                    'desc': 'Graphql은 아주 훌륭한 도구입니다',
                    'descKo': 'Graphql은 아주 훌륭한 도구입니다',
                    'descEn': 'Graphql is very good package.',
                    'price': 0,
                    'visible': False,
                    'language': 'KOREAN',
                    'owner': {
                        'username': 'testname'
                    },
                    'accepted': False,
                    'place': {
                        'name': '101'
                    },
                    'startedAt': datetime(2019, 8, 21, 13, 00).astimezone(tz=TIMEZONE).isoformat(),
                    'finishedAt': datetime(2019, 8, 21, 15, 00).astimezone(tz=TIMEZONE).isoformat(),
                    'category': {
                        'name': '머신러닝',
                        'nameKo': '머신러닝',
                        'nameEn': 'machine learning',
                        'slug': 'ML',
                        'visible': True
                    },
                    'slideUrl': 'https://slide/1',
                    'pdfUrl': 'https://pdf/1',
                    'videoUrl': 'https://video/1',
                    'difficulty': {
                        'name': '초급',
                        'nameKo': '초급',
                        'nameEn': 'beginner'
                    },
                    'recordable': True
                }
            ]
        }
        result = schema.execute(query)
        actual = loads(dumps(result.data))
        self.assertDictEqual(actual, expected)
