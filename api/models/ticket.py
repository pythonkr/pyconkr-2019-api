from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager
from api.models.program import Conference, Program


class Ticket(models.Model):
    objects = InheritanceManager()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )


class ConferenceTicket(Ticket):
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
    )

class ProgramTicket(Ticket):
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
    )

class YoungcoderTicket(ProgramTicket):
    need_laptop = models.BooleanField(default=False)
