from django.db import models
from model_utils.managers import InheritanceManager

class Program(models.Model):
    objects = InheritanceManager()
    name = models.CharField(max_length=255, null=True, blank=True)

class Presentation(Program):
    presentation_field = models.CharField(max_length=255, null=True, blank=True)

class Tutorial(Program):
    tutorial_field = models.CharField(max_length=255, null=True, blank=True)

class Sprint(Program):
    sprint_field = models.CharField(max_length=255, null=True, blank=True)

class Youngcoder(Program):
    youngcoder_field = models.CharField(max_length=255, null=True, blank=True)

class Exercise(Program):
    exercise_field = models.CharField(max_length=255, null=True, blank=True)
