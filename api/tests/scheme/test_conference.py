from json import loads, dumps
from django.utils.timezone import get_current_timezone
from api.tests.base import BaseTestCase
from api.tests.data import initialize
from api.schema import schema

TIMEZONE = get_current_timezone()


class ConferenceTest(BaseTestCase):
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
