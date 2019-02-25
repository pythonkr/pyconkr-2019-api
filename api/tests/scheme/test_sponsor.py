from datetime import datetime
from json import loads, dumps
from django.utils.timezone import get_current_timezone
from api.tests.base import BaseTestCase
from api.schema import schema

TIMEZONE = get_current_timezone()


class SponsorTestCase(BaseTestCase):
    def test_retrieve_sponsor(self):
        query = '''
                query {
                   sponsors {
                        nameKo
                        nameEn
                        descKo
                        descEn
                        url
                        level {
                            name
                            price
                            ticketCount
                        }
                        paidAt
                    }
                }
                '''

        expected = {
            'nameKo': '파이콘한국',
            'nameEn': 'Pycon Korea',
            'descKo': '파이콘 한국입니다',
            'descEn': 'we are pycon korea',
            'url': 'http://pythonkr/1',
            'level': {
                'name': '키스톤',
                'price': 20000000,
                'ticketCount': 20
            },
            'paidAt': datetime(2019, 8, 21, 13, 00).astimezone(tz=TIMEZONE).isoformat(),
        }

        result = schema.execute(query)
        actual = loads(dumps(result.data))
        self.assertIn('sponsors', actual)
        self.assertDictEqual(actual['sponsors'][0], expected)
