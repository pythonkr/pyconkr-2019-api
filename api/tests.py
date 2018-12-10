from django.test import TestCase
from api.models import Program, Presentation, Tutorial, Sprint, Youngcoder, Exercise

class ProgramTestCase(TestCase):
    def test_can_retrieve_different_models_have_same_parent(self):
        # Given
        Presentation.objects.create(name='Presentation', 
            presentation_field='Presentation Field')
        Tutorial.objects.create(name='Tutorial', 
            tutorial_field='Tutorial Field')
        Sprint.objects.create(name='Sprint', 
            sprint_field='Sprint Field')
        Youngcoder.objects.create(name='Youngcoder', 
            youngcoder_field='Youngcoder Field')
        Exercise.objects.create(name='Exercise', 
            exercise_field='Exercise Field')
        
        # When
        programs = Program.objects.select_subclasses()

        # Then
        self.assertEquals(len(programs), 5)
        self.assertTrue(any([type(program) is Presentation for program in programs]))
        self.assertTrue(any([type(program) is Tutorial for program in programs]))
        self.assertTrue(any([type(program) is Sprint for program in programs]))
        self.assertTrue(any([type(program) is Youngcoder for program in programs]))
        self.assertTrue(any([type(program) is Exercise for program in programs]))

