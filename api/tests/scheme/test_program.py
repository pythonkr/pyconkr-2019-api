from json import loads, dumps
from datetime import datetime
from django.utils.timezone import get_current_timezone
from api.tests.base import BaseTestCase
from api.tests.data import initialize
from api.schemas.schema import schema
from api.models.program import Presentation

TIMEZONE = get_current_timezone()


class ProgramTestCase(BaseTestCase):
    def setUp(self):
        initialize()

    def test_retrieve_conference(self):
        query = '''
        query {
            conference {
                name
                nameKo
                nameEn
                conferenceStartedAt
                conferenceFinishedAt
                sprintStartedAt
                sprintFinishedAt
                tutorialStartedAt
                tutorialFinishedAt
            }
        }
        '''

        expected = {
            'conference': {
                'name': '파이콘 한국 2019',
                'nameKo': '파이콘 한국 2019',
                'nameEn': 'Pycon Korea 2019',
                'conferenceStartedAt': '2019-08-10',
                'conferenceFinishedAt': '2019-08-11',
                'sprintStartedAt': '2019-08-09',
                'sprintFinishedAt': '2019-08-09',
                'tutorialStartedAt': '2019-08-08',
                'tutorialFinishedAt': '2019-08-09'
            }
        }
        result = schema.execute(query)
        actual = loads(dumps(result.data))
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
                    'language': Presentation.LANGUAGE_KOREAN,
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

    def test_retrieve_sponsor(self):
        query = '''
        query {
            conference {
                name_ko
                desc_ko
                name_en
                desc_en
                image
                url
                level {
                    name
                    desc
                    price
                    ticket_count
                }
                paid_at
                ticket_users
            }
        }
        '''

        expected = {
            'name_ko' : '파이콘준비위원회',
            'desc_ko' : '파이콘을 준비하는 준비위원회입니다.',
            'name_en' : 'PyconKr',
            'desc_en' : 'The people who want to open python conference.',
            'image'   : 'img',
            'url'     : 'http://pythonkr/1',
            'level'   : {
                        'name' : '키스톤',
                        'desc' : '가장돈은 많이 낸 분들이죠',
                        'price': '20000000',
                        'ticket_count' : '20'
                        },
            'paid_at' : 'datetime(2019, 8, 21, 13, 00).astimezone(tz=timezone)',
            'ticket_users' : 'user'

        }


        result = schema.execute(query)
        actual = loads(dumps(result.data))
        self.assertDictEqual(actual, expected)
