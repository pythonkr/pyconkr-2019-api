from django.test import TestCase

# pylint: disable=invalid-name

class BaseTestCase(TestCase):
    fixtures = [
        'api/tests/fixtures/oauthsetting.json',
        'api/tests/fixtures/conference.json',
        'api/tests/fixtures/user.json',
        'api/tests/fixtures/category.json',
        'api/tests/fixtures/difficulty.json',
        'api/tests/fixtures/place.json',
        'api/tests/fixtures/program.json',
        'api/tests/fixtures/sponsor.json',
    ]

    def assertHasAnyType(self, arr, cls):
        self.assertTrue(any([isinstance(item, cls) for item in arr]))
