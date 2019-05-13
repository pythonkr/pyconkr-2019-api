from datetime import timedelta
from unittest import mock

from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from django.utils.timezone import now
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.tests.base import BaseTestCase
from ticket.models import TicketProduct, Ticket, TransactionMixin
from ticket.ticket_queries import BUY_TICKET, MY_TICKETS, CANCEL_TICKET

TIMEZONE = get_current_timezone()

UserModel = get_user_model()


class TicketTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)
        self.product = self.create_ticket_product()

    def create_ticket_product(self):
        product = TicketProduct(
            name='얼리버드 티켓', total=3,
            owner=self.user, price='1000')
        product.ticket_open_at = now() - timedelta(days=2)
        product.ticket_close_at = now() + timedelta(days=2)
        product.cancelable_date = now() + timedelta(days=1)
        product.save()
        return product

    @mock.patch('ticket.schemas.config')
    @mock.patch('ticket.schemas.Iamport', autospec=True)
    def test_buy_early_bird_ticket(self, mock_iamport, mock_config):
        # Given
        self.mock_config_and_iamporter(mock_config, mock_iamport)

        variables = {
            "productId": str(self.product.id),
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
    @mock.patch('ticket.schemas.Iamport', autospec=True)
    def test_buy_early_bird_ticket_with_tshirt_size(self, mock_iamport, mock_config):
        # Given
        self.mock_config_and_iamporter(mock_config, mock_iamport)

        variables = {
            'productId': str(self.product.id),
            'payment': {
                'isDomesticCard': True,
                'cardNumber': '0000-0000-0000-0000',
                'expiry': '2022-12',
                'birth': '880101',
                'pwd2digit': '11'
            },
            'options': '{"tshirt_size": "M"}'
        }

        response = self.client.execute(BUY_TICKET, variables)
        data = response.data
        self.assertIsNotNone(data['buyTicket'])
        tickets = Ticket.objects.all()
        self.assertEqual(1, tickets.count())
        self.assertEqual('M', tickets[0].options['tshirt_size'])

    @mock.patch('ticket.schemas.config')
    @mock.patch('ticket.schemas.Iamport', autospec=True)
    def test_buy_early_bird_ticket_foreign(self, mock_iamport, mock_config):
        # Given
        self.mock_config_and_iamporter(mock_config, mock_iamport)

        variables = {
            "productId": str(self.product.id),
            "payment": {
                "isDomesticCard": False,
                "cardNumber": "0000-0000-0000-0000",
                "expiry": "2022-12",
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
    @mock.patch('ticket.schemas.Iamport', autospec=True)
    def test_GIVEN_카드_정보_일부_누락_buy_early_bird_ticket_foreign_THEN_에러발생(self, mock_iamport, mock_config):
        # Given
        self.mock_config_and_iamporter(mock_config, mock_iamport)

        variables = {
            "productId": str(self.product.id),
            "payment": {
                "isDomesticCard": False,
                "expiry": "2022-12",
            }
        }

        result = self.client.execute(BUY_TICKET, variables)
        self.assertIsNotNone(result.errors)

    def mock_config_and_iamporter(self, mock_config, mock_iamport):
        mock_config.return_value = {
            'IMP_DOM_API_KEY': 'KEY',
            'IMP_DOM_API_SECRET': 'SECRET',
            'IMP_INTL_API_KEY': 'KEY',
            'IMP_INTL_API_SECRET': 'SECRET'
        }
        iamport_instance = mock_iamport.return_value
        response = {
            'amount': '60000',
            'name': 'name',
            'status': 'paid',
            'paid_at': 1556189352,
            'receipt_url': 'receipt_url',
            'pg_tid': 'pg_tid',
            'imp_uid': 'imp_uid',
            'merchant_uid': 'pyconkr_1556189352'
        }
        iamport_instance.pay_onetime.return_value = response
        iamport_instance.pay_foreign.return_value = response

        cancel_response = {
            'amount': '60000',
            'name': 'name',
            'status': 'cancelled',
            'paid_at': 1556189352,
            'receipt_url': 'receipt_url',
            'cancelled_at': 1556189390,
            'cancel_receipt_urls': ['cancel_receipt_urls'],
            'pg_tid': 'pg_tid',
            'imp_uid': 'imp_uid',
            'merchant_uid': 'pyconkr_1556189352'
        }
        iamport_instance.cancel.return_value = cancel_response

    @mock.patch('ticket.schemas.config')
    @mock.patch('ticket.schemas.Iamport', autospec=True)
    def test_GIVEN_카드_정보_일부_누락_WHEN_buy_early_bird_ticket_THEN_에러발생1(self, mock_iamport, mock_config):
        # Given

        self.mock_config_and_iamporter(mock_config, mock_iamport)

        variables = {
            "productId": str(self.product.id),
            "payment": {
                "isDomesticCard": True,
                "cardNumber": "0000-0000-0000-0000",
                "expiry": "2022-12",
                "pwd2digit": "11"
            }
        }

        result = self.client.execute(BUY_TICKET, variables)
        self.assertIsNotNone(result.errors)

    @mock.patch('ticket.schemas.config')
    @mock.patch('ticket.schemas.Iamport', autospec=True)
    def test_GIVEN_카드_정보_일부_누락_WHEN_buy_early_bird_ticket_THEN_에러발생2(self, mock_iamport, mock_config):
        # Given
        self.mock_config_and_iamporter(mock_config, mock_iamport)

        variables = {
            "productId": str(self.product.id),
            "payment": {
                "isDomesticCard": True,
                "cardNumber": "0000-0000-0000-0000",
                "expiry": "2022-12",
                "birth": "880101",
            }
        }

        result = self.client.execute(BUY_TICKET, variables)
        self.assertIsNotNone(result.errors)

    def test_WHEN_티켓을_구매했으면_get_my_tickets_THEN_이력_출력(self):
        product = self.create_ticket_product()
        Ticket.objects.create(
            product=product, owner=self.user, status=TransactionMixin.STATUS_PAID)

        result = self.client.execute(MY_TICKETS)
        data = result.data
        self.assertIsNotNone(data['myTickets'])
        self.assertEqual(1, len(data['myTickets']))

    @mock.patch('ticket.schemas.config')
    @mock.patch('ticket.schemas.Iamport', autospec=True)
    def test_cancel_ticket(self, mock_iamport, mock_config):
        self.mock_config_and_iamporter(mock_config, mock_iamport)

        product = self.create_ticket_product()
        ticket = Ticket.objects.create(
            product=product, owner=self.user, status=TransactionMixin.STATUS_PAID,
            imp_uid='imp_testtest')
        variables = {
            "ticketId": ticket.id,
        }
        result = self.client.execute(CANCEL_TICKET, variables)
        data = result.data
        self.assertIsNotNone(data['cancelTicket'])
        self.assertIsNotNone(data['cancelTicket']['ticket'])
        self.assertEqual(Ticket.STATUS_CANCELLED.upper(),
                         data['cancelTicket']['ticket']['status'])

    @mock.patch('ticket.schemas.config')
    @mock.patch('ticket.schemas.Iamport', autospec=True)
    def test_cancel_ticket_취소_가능_기한이_지났음(self, mock_iamport, mock_config):
        self.mock_config_and_iamporter(mock_config, mock_iamport)
        product = self.create_ticket_product()
        product.cancelable_date = now() - timedelta(days=1)
        product.save()

        ticket = Ticket.objects.create(
            product=product, owner=self.user, status=TransactionMixin.STATUS_PAID,
            imp_uid='imp_testtest')
        variables = {
            "ticketId": ticket.id,
        }
        result = self.client.execute(CANCEL_TICKET, variables)
        self.assertIsNotNone(result.errors)

    @mock.patch('ticket.schemas.config')
    @mock.patch('ticket.schemas.Iamport', autospec=True)
    def test_cancel_ticket_다른_유저의_티켓(self, mock_iamport, mock_config):
        self.mock_config_and_iamporter(mock_config, mock_iamport)
        product = self.create_ticket_product()
        another_user = get_user_model().objects.create(
            username='another',
            email='another@pycon.kr')

        ticket = Ticket.objects.create(
            product=product, owner=another_user, status=TransactionMixin.STATUS_PAID,
            imp_uid='imp_testtest')
        variables = {
            "ticketId": ticket.id,
        }
        result = self.client.execute(CANCEL_TICKET, variables)
        self.assertIsNotNone(result.errors)

    @mock.patch('ticket.schemas.config')
    @mock.patch('ticket.schemas.Iamport', autospec=True)
    def test_cancel_ticket_두번호출_시_에러(self, mock_iamport, mock_config):
        self.mock_config_and_iamporter(mock_config, mock_iamport)

        product = self.create_ticket_product()
        ticket = Ticket.objects.create(
            product=product, owner=self.user, status=TransactionMixin.STATUS_PAID,
            imp_uid='imp_testtest')
        variables = {
            "ticketId": ticket.id,
        }
        self.client.execute(CANCEL_TICKET, variables)
        result = self.client.execute(CANCEL_TICKET, variables)
        self.assertIsNotNone(result.errors)
