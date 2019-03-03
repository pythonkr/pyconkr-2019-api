from json import loads, dumps
from django.utils.timezone import get_current_timezone
from api.tests.base import BaseTestCase
from api.schema import schema

TIMEZONE = get_current_timezone()


class ConferenceTest(BaseTestCase):
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
                'conferenceStartedAt': '2019-08-17',
                'conferenceFinishedAt': '2019-08-18',
                'sprintStartedAt': '2019-08-15',
                'sprintFinishedAt': '2019-08-16',
                'tutorialStartedAt': '2019-08-15',
                'tutorialFinishedAt': '2019-08-16'
            }
        }
        result = schema.execute(query)
        actual = loads(dumps(result.data))
        self.assertDictEqual(actual, expected)
