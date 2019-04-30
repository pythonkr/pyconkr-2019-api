from datetime import timedelta
from unittest import mock

from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from django.utils.timezone import now
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.models import Ticket, TicketProduct
from api.tests.base import BaseTestCase
from api.tests.scheme.ticket_queries import BUY_TICKET

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
    def test_buy_early_bird_ticket(self, mock_iamporter, mock_settings):
        # Given
        product = TicketProduct(
            name='얼리버드 티켓', total=3,
            owner=self.user, price='1000')
        product.ticket_open_at = now() - timedelta(days=2)
        product.ticket_close_at = now() + timedelta(days=2)
        product.save()
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
            "productId": str(product.id),
            "payment": {
                "cardNumber": "0000-0000-0000-0000",
                "expiry": "2022-12",
                "birth": "880101",
                "pwd2digit": "11"
            },
            'options': '{}'
        }

        response = self.client.execute(BUY_TICKET, variables)
        data = response.data
        self.assertIsNotNone(data['buyTicket'])
        self.assertIsNotNone(data['buyTicket']['ticket'])
        self.assertEqual(data['buyTicket']['ticket']['pgTid'], 'pg_tid')
        self.assertIsNotNone(data['buyTicket']['ticket']['receiptUrl'])

        self.assertEqual(1, Ticket.objects.all().count())