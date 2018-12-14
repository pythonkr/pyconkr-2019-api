from django.test import TestCase

# pylint: disable=invalid-name


class BaseTestCase(TestCase):
    def assertHasAnyType(self, arr, cls):
        self.assertTrue(any([isinstance(item, cls) for item in arr]))
