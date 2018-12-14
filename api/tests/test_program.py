from api.models import Program, Conference, Tutorial, Sprint, Youngcoder, Exercise
from api.tests.base import BaseTestCase
from api.tests.common import create_conference, create_exercise, create_sprint, \
    create_tutorial, create_youngcoder


class ProgramTestCase(BaseTestCase):
    def test_can_retrieve_different_programs_have_same_parent(self):
        # Given
        # 동일한 Program을 상속받은 5개의 서로 다른 Model을 1개씩 추가
        create_conference()
        create_tutorial()
        create_sprint()
        create_youngcoder()
        create_exercise()

        # When
        # 저장된 Program을 다 받아옴
        programs = Program.objects.select_subclasses()

        # Then
        # 5개가 모두 저장되어 있으면 각자의 Class로 반환됨
        self.assertEqual(len(programs), 5)
        self.assertHasAnyType(programs, Conference)
        self.assertHasAnyType(programs, Tutorial)
        self.assertHasAnyType(programs, Sprint)
        self.assertHasAnyType(programs, Youngcoder)
        self.assertHasAnyType(programs, Exercise)
