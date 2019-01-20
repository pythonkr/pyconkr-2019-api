from api.tests.base import BaseTestCase
from api.tests.data import initialize
from api.schema import schema


class ProgramTestCase(BaseTestCase):
    def setUp(self):
        initialize()

    def test_retrive_presentation(self):
        query = '''
        query {
            presentations {
                name
            }
        }
        '''

        expected = {
            'presentations': [
                {
                    'name': 'Graphql로 api를 만들어보자'
                },
                {
                    'name': 'django로 웹 개발하기'
                },
            ]
        }
        result = schema.execute(query)
        self.assertEqual(result.data, expected)
