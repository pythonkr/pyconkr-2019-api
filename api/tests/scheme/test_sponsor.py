from datetime import datetime
from json import loads, dumps
from django.utils.timezone import get_current_timezone
from api.tests.base import BaseTestCase
from api.tests.data import initialize
from api.schemas.schema import schema

TIMEZONE = get_current_timezone()


class SponsorTestCase(BaseTestCase):
    def setUp(self):
        initialize()

    def test_retrieve_sponsor(self):
        query = '''
        query {
            sponsors {
                nameKo
            }
        }
        '''

        expected = {
            'nameKo': '파이콘준비위원회',
            'descKo': '파이콘을 준비하는 준비위원회입니다.',
            'nameEn': 'PyconKr',
            'descEn': 'The people who want to open python conference.',
            'image': 'img',
            'url': 'http://pythonkr/1',
            'level': {
                'name': '키스톤',
                'desc': '가장돈은 많이 낸 분들이죠',
                'price': '20000000',
                'ticketCount': '20'
            },
            'paidAt': datetime(2019, 8, 21, 13, 00).astimezone(tz=TIMEZONE).isoformat(),
            'ticketUsers': 'user'

        }

        result = schema.execute(query)
        actual = loads(dumps(result.data))
        self.assertDictEqual(actual, expected)

    def test_스폰서_리스트_나열하기(self):
        query = '''
        query {
            sponsors {
                slug
                name
                desc
                image
                url
                level
                paid_at
                ticket_users
            }
        }
        '''

        expected = {
            'sponsors': [
                {
                    'slug': 'WADIZ_slug',
                    'name': 'WADIZ',
                    'desc': '크라우드펀딩 넘버원 와디즈',
                    'image': './',
                    'url': 'www.wadiz.co.kr',
                    'level': '5',
                    'paid_at': '2019-01-01',
                    'ticket_users': ['test@test.com']
                }
            ]
        }
        result = schema.execute(query)
        self.assertEqual(result.data, expected)
