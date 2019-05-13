from datetime import timedelta
from unittest import mock

from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from django.utils.timezone import now
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.tests.base import BaseTestCase
from ticket.models import TicketProduct, Ticket
from ticket.ticket_queries import BUY_TICKET

TIMEZONE = get_current_timezone()

UserModel = get_user_model()


class TicketTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)

    @mock.patch('ticket.schemas.config')
    @mock.patch('ticket.schemas.Iamporter', autospec=True)
    def test_buy_early_bird_ticket(self, mock_iamporter, mock_config):
        # Given
        product = TicketProduct(
            name='얼리버드 티켓', total=3,
            owner=self.user, price='1000')
        product.ticket_open_at = now() - timedelta(days=2)
        product.ticket_close_at = now() + timedelta(days=2)
        product.save()
        mock_config.return_value = {
            'IMP_DOM_API_KEY': 'KEY',
            'IMP_DOM_API_SECRET': 'SECRET',
            'IMP_INTL_API_KEY': 'KEY',
            'IMP_INTL_API_SECRET': 'SECRET'
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
                "isDomesticCard": True,
                "cardNumber": "0000-0000-0000-0000",
                "expiry": "2022-12",
                "birth": "880101",
                "pwd2digit": "11"
            }
        }

        response = self.client.execute(BUY_TICKET, variables)
        data = response.data
        self.assertIsNotNone(data['buyTicket'])
        self.assertIsNotNone(data['buyTicket']['ticket'])
        self.assertEqual(data['buyTicket']['ticket']['pgTid'], 'pg_tid')
        self.assertIsNotNone(data['buyTicket']['ticket']['receiptUrl'])

        self.assertEqual(1, Ticket.objects.all().count())

    @mock.patch('ticket.schemas.config')
    @mock.patch('ticket.schemas.Iamporter', autospec=True)
    def test_GIVEN_카드_정보_일부_누락_WHEN_buy_early_bird_ticket_THEN_에러발생(self, mock_iamporter, mock_config):
        # Given
        product = TicketProduct(
            name='얼리버드 티켓', total=3,
            owner=self.user, price='1000')
        product.ticket_open_at = now() - timedelta(days=2)
        product.ticket_close_at = now() + timedelta(days=2)
        product.save()
        mock_config.return_value = {
            'IMP_DOM_API_KEY': 'KEY',
            'IMP_DOM_API_SECRET': 'SECRET',
            'IMP_INTL_API_KEY': 'KEY',
            'IMP_INTL_API_SECRET': 'SECRET'
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
                "isDomesticCard": True,
                "cardNumber": "0000-0000-0000-0000",
                "expiry": "2022-12",
                "pwd2digit": "11"
            }
        }

        result = self.client.execute(BUY_TICKET, variables)
        self.assertIsNotNone(result.errors)
