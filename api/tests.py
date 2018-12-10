from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Program, Conference, Tutorial, Sprint, Youngcoder, Exercise
from api.models import Ticket, ConferenceTicket, YoungcoderTicket

class ProgramTestCase(TestCase):
    def test_can_retrieve_different_programs_have_same_parent(self):
        # Given
        # 동일한 Program을 상속받은 5개의 서로 다른 Model을 1개씩 추가
        self._create_conference()
        self._create_tutorial()
        self._create_sprint()
        self._create_youngcoder()
        self._create_exercise()
        
        # When
        # 저장된 Program을 다 받아옴
        programs = Program.objects.select_subclasses()

        # Then
        # 5개가 모두 저장되어 있으면 각자의 Class로 반환됨
        self.assertEquals(len(programs), 5)
        self.assertHasAnyType(programs, Conference)
        self.assertHasAnyType(programs, Tutorial)
        self.assertHasAnyType(programs, Sprint)
        self.assertHasAnyType(programs, Youngcoder)
        self.assertHasAnyType(programs, Exercise)

    def test_can_retrieve_different_tickets_have_same_parent(self):
        # Given
        # 동일한 Ticket을 상속받은 2개의 서로 다른 Model을 생성
        # Youngcoder는 need_labtop 필드가 추가되어 있음
        user = User.objects.create_user('testname', 'test@test.com', 'testpassword')
        conference = self._create_conference()
        ConferenceTicket.objects.create(user=user, program=conference)
        youngcoder = self._create_youngcoder()
        YoungcoderTicket.objects.create(user=user, program=youngcoder, need_laptop=True)
        
        # When
        # User에 속한 Ticket을 모두 받아옴
        tickets = user.ticket_set.all().select_subclasses()

        # Then
        # 2개의 Ticket이 정상적으로 저장되어 있으며, 
        # 특화된 Field도 잘 반영되어 있음
        self.assertEquals(len(tickets), 2)
        self.assertHasAnyType(tickets, ConferenceTicket)
        self.assertHasAnyType(tickets, YoungcoderTicket)
        youngcoder_ticket = self._get_first_class_item_from_arr(tickets, YoungcoderTicket)
        self.assertTrue(youngcoder_ticket.need_laptop)


    def assertHasAnyType(self, arr, cls):
        self.assertTrue(any([type(item) is cls for item in arr]))

    def _create_conference(self, name='Conference', field='Conference Field'):
        return Conference.objects.create(name=name, conference_field=field)
    
    def _create_tutorial(self, name='Tutorial', field='Tutorial Field'):
        return Tutorial.objects.create(name=name, tutorial_field=field)
    
    def _create_sprint(self, name='Sprint'):
        return Sprint.objects.create(name=name)

    def _create_youngcoder(self, name='Youngcoder'):
        return Youngcoder.objects.create(name=name)
    
    def _create_exercise(self, name='Exercise'):
        return Exercise.objects.create(name=name)

    def _get_first_class_item_from_arr(self, arr, cls):
        items = [item for item in arr if type(item) is cls]
        if len(items) > 0:
            return items[0]
        return None