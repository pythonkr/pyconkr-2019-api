from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from django.utils.timezone import now
from graphql_jwt.testcases import JSONWebTokenTestCase

from api.tests.base import BaseTestCase
from ticket.models import TicketProduct, Ticket, TransactionMixin
from ticket.ticket_queries import TICKET_PRODUCTS

TIMEZONE = get_current_timezone()

UserModel = get_user_model()


class TicketProductTestCase(BaseTestCase, JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='develop_github_123',
            email='me@pycon.kr')
        self.client.authenticate(self.user)

    def create_ticket_product(self, product_type, owner=None, name='티켓', price=50000, total=3, is_unique_in_type=False):
        product = TicketProduct(
            type=product_type, name=name, total=total,
            owner=owner, price=price,
            is_unique_in_type=is_unique_in_type)
        product.ticket_open_at = now() - timedelta(days=2)
        product.ticket_close_at = now() + timedelta(days=2)
        product.save()
        return product

    def test_get_ticket_products(self):
        self.create_ticket_product(
            name='얼리버드 티켓', product_type=TicketProduct.TYPE_CONFERENCE,
            is_unique_in_type=True)
        self.create_ticket_product(
            name='일반 티켓', product_type=TicketProduct.TYPE_CONFERENCE,
            is_unique_in_type=True)

        self.create_ticket_product(
            name='튜토리얼', product_type=TicketProduct.TYPE_TUTORIAL, owner=self.user)

        result = self.client.execute(TICKET_PRODUCTS)
        data = result.data
        self.assertIsNotNone(data['conferenceProducts'])
        self.assertEqual(2, len(data['conferenceProducts']))
        self.assertEqual('CONFERENCE', data['conferenceProducts'][0]['type'])

    def test_GIVEN_unique_in_type이면_WHEN_get_ticket_products_THEN_같은_타입의_isPurchased도_true(self):
        product = self.create_ticket_product(
            name='얼리버드 티켓', product_type=TicketProduct.TYPE_CONFERENCE,
            is_unique_in_type=True)
        self.create_ticket_product(
            name='일반 티켓', product_type=TicketProduct.TYPE_CONFERENCE,
            is_unique_in_type=True)
        Ticket.objects.create(
            product=product, owner=self.user, status=TransactionMixin.STATUS_PAID)

        result = self.client.execute(TICKET_PRODUCTS)
        data = result.data
        self.assertEqual(1, data['conferenceProducts'][0]['purchaseCount'])
        self.assertEqual(True, data['conferenceProducts'][0]['isPurchased'])
        self.assertEqual(True, data['conferenceProducts'][1]['isPurchased'])

    def test_GIVEN_unique_in_type이라도_type이_다르면_WHEN_get_ticket_products_THEN_isPurchased가_false(self):
        product = self.create_ticket_product(
            name='얼리버드 티켓', product_type=TicketProduct.TYPE_CONFERENCE,
            is_unique_in_type=True)
        self.create_ticket_product(
            name='튜토리얼', product_type=TicketProduct.TYPE_TUTORIAL, owner=self.user)
        Ticket.objects.create(
            product=product, owner=self.user, status=TransactionMixin.STATUS_PAID)

        result = self.client.execute(TICKET_PRODUCTS)
        data = result.data
        self.assertEqual(1, data['conferenceProducts'][0]['purchaseCount'])
        self.assertEqual(True, data['conferenceProducts'][0]['isPurchased'])
        self.assertEqual(False, data['tutorialProducts'][0]['isPurchased'])

    def test_WHEN_티켓을_구매했으면_get_ticket_products_THEN_구매_개수_출력(self):
        product = self.create_ticket_product(
            name='얼리버드 티켓', product_type=TicketProduct.TYPE_CONFERENCE)
        Ticket.objects.create(
            product=product, owner=self.user, status=TransactionMixin.STATUS_PAID)

        result = self.client.execute(TICKET_PRODUCTS)
        data = result.data
        self.assertEqual(1, data['conferenceProducts'][0]['purchaseCount'])
        self.assertEqual(True, data['conferenceProducts'][0]['isPurchased'])

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
        self.assertEqual(False, data['conferenceProducts'][0]['isPurchased'])

    def test_WHEN_매진이면_get_ticket_products_THEN_매진이라고_반환(self):
        product = self.create_ticket_product(
            name='얼리버드 티켓', product_type=TicketProduct.TYPE_CONFERENCE, total=1)
        user = get_user_model().objects.create(
            username='other_user',
            email='other@pycon.kr')
        Ticket.objects.create(
            product=product, owner=user, status=TransactionMixin.STATUS_PAID)

        result = self.client.execute(TICKET_PRODUCTS)
        data = result.data
        self.assertTrue(data['conferenceProducts'][0]['isSoldOut'])
        self.assertEqual(0, data['conferenceProducts'][0]['remainingCount'])

    def test_WHEN_팔리기전에는_get_ticket_products_THEN_total과_remaining_count_가_같음(self):
        self.create_ticket_product(
            name='얼리버드 티켓', product_type=TicketProduct.TYPE_CONFERENCE, total=3)

        result = self.client.execute(TICKET_PRODUCTS)
        data = result.data
        self.assertFalse(data['conferenceProducts'][0]['isSoldOut'])
        self.assertEqual(3, data['conferenceProducts'][0]['remainingCount'])

    def test_get_ticket_products_with_ticket_for(self):
        product = self.create_ticket_product(
            name='얼리버드 티켓', product_type=TicketProduct.TYPE_CONFERENCE)
        product.ticket_for.add(self.user)
        result = self.client.execute(TICKET_PRODUCTS)
        data = result.data
        self.assertEqual(1, len(data['conferenceProducts']))

    def test_get_ticket_products_with_ticket_for_호출하는_사용자가_ticket_for에_없을_때(self):
        product = self.create_ticket_product(
            name='얼리버드 티켓', product_type=TicketProduct.TYPE_CONFERENCE)
        user = get_user_model().objects.create(
            username='other_user',
            email='other@pycon.kr')
        product.ticket_for.add(user)
        result = self.client.execute(TICKET_PRODUCTS)
        data = result.data
        self.assertEqual(0, len(data['conferenceProducts']))
