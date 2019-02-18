from api.models.programs import Program, Tutorial, Sprint, Youngcoder, Exercise
from api.tests.base import BaseTestCase
from api.tests.common import create_exercise, create_sprint, \
    create_tutorial, create_youngcoder


class ProgramTestCase(BaseTestCase):
    def test_can_retrieve_different_programs_have_same_parent(self):
        # Given
        # 동일한 Program을 상속받은 4개의 서로 다른 Model을 1개씩 추가
        create_tutorial()
        create_sprint()
        create_youngcoder()
        create_exercise()

        # When
        # 저장된 Program을 다 받아옴
        programs = Program.objects.select_subclasses()

        # Then
        # 4개가 모두 저장되어 있으면 각자의 Class로 반환됨
        self.assertEqual(len(programs), 4)
        self.assertHasAnyType(programs, Tutorial)
        self.assertHasAnyType(programs, Sprint)
        self.assertHasAnyType(programs, Youngcoder)
        self.assertHasAnyType(programs, Exercise)
