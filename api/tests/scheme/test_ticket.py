from unittest import mock

from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.models import EarlyBirdTicket
from api.tests.base import BaseTestCase
from api.tests.scheme.ticket_queries import BUY_EARLY_BIRD_TICKET

TIMEZONE = get_current_timezone()

UserModel = get_user_model()


class TicketTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)

    @mock.patch('api.schemas.ticket.settings')
    @mock.patch('api.schemas.ticket.Iamporter', autospec=True)
    def test_create_proposal(self, mock_iamporter, mock_settings):
        # Given
        mock_settings.return_value = {
            'IMP_KEY': 'KEY',
            'IMP_SECRET': 'SECRET'
        }
        iamporter_instance = mock_iamporter.return_value
        iamporter_instance.create_payment.return_value = {
            'amount': '60000',
            'name': 'name',
            'status': 'paid',
            'paid_at': 1556189352,
            'receipt_url': 'receipt_url',
            'pg_tid': 'pg_tid',
            'imp_uid': 'imp_uid'
        }

        variables = {
            "payment": {
                "cardNumber": "0000-0000-0000-0000",
                "expiry": "2022-12",
                "birth": "880101",
                "pwd2digit": "11"
            }
        }

        response = self.client.execute(BUY_EARLY_BIRD_TICKET, variables)
        data = response.data
        self.assertIsNotNone(data['buyEarlyBirdTicket'])
        self.assertIsNotNone(data['buyEarlyBirdTicket']['ticket'])
        self.assertEqual(data['buyEarlyBirdTicket']['ticket']['pgTid'], 'pg_tid')
        self.assertIsNotNone(data['buyEarlyBirdTicket']['ticket']['receiptUrl'])

        self.assertEqual(1, EarlyBirdTicket.objects.all().count())
