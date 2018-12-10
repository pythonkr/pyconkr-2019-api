from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager

class Program(models.Model):
    objects = InheritanceManager()
    name = models.CharField(max_length=255, null=True, blank=True)

class Conference(Program):
    conference_field = models.CharField(max_length=255, null=True, blank=True)

class Tutorial(Program):
    tutorial_field = models.CharField(max_length=255, null=True, blank=True)

class Sprint(Program):
    pass

class Youngcoder(Program):
    pass

class Exercise(Program):
    pass

class Ticket(models.Model):
    objects = InheritanceManager()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
    )

class ConferenceTicket(Ticket):
    pass

class YoungcoderTicket(Ticket):
    need_laptop = models.BooleanField(default=False)



