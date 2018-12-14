from django.contrib.auth.models import User
from api.models import ConferenceTicket, YoungcoderTicket
from api.tests.base import BaseTestCase
from api.tests.common import create_conference, create_youngcoder, get_first_class_item_from_arr


class TicketTestCase(BaseTestCase):
    def test_can_retrieve_different_tickets_have_same_parent(self):
        # Given
        # 동일한 Ticket을 상속받은 2개의 서로 다른 Model을 생성
        # Youngcoder는 need_labtop 필드가 추가되어 있음
        user = User.objects.create_user(
            'testname', 'test@test.com', 'testpassword')
        conference = create_conference()
        ConferenceTicket.objects.create(user=user, program=conference)
        youngcoder = create_youngcoder()
        YoungcoderTicket.objects.create(
            user=user, program=youngcoder, need_laptop=True)

        # When
        # User에 속한 Ticket을 모두 받아옴
        tickets = user.ticket_set.all().select_subclasses()

        # Then
        # 2개의 Ticket이 정상적으로 저장되어 있으며,
        # 특화된 Field도 잘 반영되어 있음
        self.assertEqual(len(tickets), 2)
        self.assertHasAnyType(tickets, ConferenceTicket)
        self.assertHasAnyType(tickets, YoungcoderTicket)
        youngcoder_ticket = get_first_class_item_from_arr(
            tickets, YoungcoderTicket)
        self.assertTrue(youngcoder_ticket.need_laptop)
