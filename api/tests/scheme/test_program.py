from datetime import datetime
from api.tests.base import BaseTestCase
from api.tests.data import initialize
from api.schema import schema
from api.models.program import Presentation


class ProgramTestCase(BaseTestCase):
    def setUp(self):
        initialize()

    def test_retrive_presentation(self):
        query = '''
        query {
            presentations {
                nameKo
                descKo
                nameEn
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
                    slug
                    visible
                }
                slideUrl
                pdfUrl
                videoUrl
                difficulty {
                    nameEn
                    nameKo
                }
                recordable
            }
        }
        '''

        expected = {
            'presentations': [
                {
                    'nameKo': 'Graphql로 api를 만들어보자',
                    'descKo': 'Graphql은 아주 훌륭한 도구입니다',
                    'nameEn': 'Make api using Graphql',
                    'descEn': 'Graphql is very good package.',
                    'price': 0,
                    'visible': False,
                    'language': Presentation.LANGUAGE_KOREAN,
                    'owner': {
                        'username': 'testname'
                    },
                    'accepted': False,
                    'place': {
                        'name': '101'
                    },
                    'startedAt': datetime(2017, 8, 21, 13, 00),
                    'finishedAt': datetime(2017, 8, 21, 15, 00),
                    'category': {
                        'name': 'machine learning',
                        'slug': 'ML',
                        'visible': True
                    },
                    'slideUrl': 'https://slide/1',
                    'pdfUrl': 'https://pdf/1',
                    'videoUrl': 'https://video/1',
                    'difficulty': {
                        'nameEn': 'beginner',
                        'nameEo': '초급'
                    },
                    'recordable': True
                }
            ]
        }
        result = schema.execute(query)

        self.assertEqual(sorted(dict(result.data)), sorted(expected))
