from api.tests.base import BaseTestCase
from api.tests.data import initialize
from api.schema import schema


class ProgramTestCase(BaseTestCase):
    def setUp(self):
        initialize()

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
