from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from django.utils.timezone import now
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.tests.base import BaseTestCase
from ticket.models import TicketProduct, Ticket, TransactionMixin, OptionDesc
from ticket.ticket_queries import TICKET_PRODUCTS

TIMEZONE = get_current_timezone()

UserModel = get_user_model()


class TicketProductTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)

    def create_ticket_product(self, product_type, owner=None, name='티켓', price=50000, total=3):
        product = TicketProduct(
            type=product_type, name=name, total=total,
            owner=owner, price=price)
        product.ticket_open_at = now() - timedelta(days=2)
        product.ticket_close_at = now() + timedelta(days=2)
        product.save()
        return product

    def test_get_ticket_products(self):
        self.create_ticket_product(
            name='얼리버드 티켓', product_type=TicketProduct.TYPE_CONFERENCE)
        self.create_ticket_product(
            name='일반 티켓', product_type=TicketProduct.TYPE_CONFERENCE)

        self.create_ticket_product(
            name='튜토리얼', product_type=TicketProduct.TYPE_TUTORIAL, owner=self.user)

        result = self.client.execute(TICKET_PRODUCTS)
        data = result.data
        self.assertIsNotNone(data['conferenceProducts'])
        self.assertEqual(2, len(data['conferenceProducts']))
        self.assertEqual('CONFERENCE', data['conferenceProducts'][0]['type'])

    def test_WHEN_티켓을_구매했으면_get_ticket_products_THEN_구매_개수_출력(self):
        product = self.create_ticket_product(
            name='얼리버드 티켓', product_type=TicketProduct.TYPE_CONFERENCE)
        Ticket.objects.create(
            product=product, owner=self.user, status=TransactionMixin.STATUS_PAID)

        result = self.client.execute(TICKET_PRODUCTS)
        data = result.data
        self.assertEqual(1, data['conferenceProducts'][0]['purchaseCount'])

    def test_WHEN_다른_유저가_티켓을_구매했으면_get_ticket_products_THEN_영향_안미침(self):
        product = self.create_ticket_product(
            name='얼리버드 티켓', product_type=TicketProduct.TYPE_CONFERENCE)
        user = get_user_model().objects.create(
            username='other_user',
            email='other@pycon.kr')
        Ticket.objects.create(
            product=product, owner=user, status=TransactionMixin.STATUS_PAID)

        result = self.client.execute(TICKET_PRODUCTS)
        data = result.data
        self.assertEqual(0, data['conferenceProducts'][0]['purchaseCount'])

    def test_get_ticket_products_with_optiondesc_set(self):
        product = self.create_ticket_product(
            name='얼리버드 티켓', product_type=TicketProduct.TYPE_CONFERENCE)
        OptionDesc.objects.create(
            type=OptionDesc.TYPE_BOOL, product=product, key='t_shirt_size',
            name='티셔츠 사이즈', desc='티셔츠사이즈입니다.')
        result = self.client.execute(TICKET_PRODUCTS)
        data = result.data
        self.assertIsNotNone(data['conferenceProducts'])
        self.assertEqual('티셔츠 사이즈',
                         data['conferenceProducts'][0]['optiondescSet'][0]['name'])
