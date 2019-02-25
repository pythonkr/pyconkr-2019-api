from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField as SorlImageField


class SponsorLevel(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(default=0)
    limit = models.IntegerField(default=0, help_text='스폰서 등급의 구좌수')
    ticket_count = models.IntegerField(default=0, help_text='스폰서에게 제공되는 티켓의 수')
    presentation_count = models.IntegerField(default=0, help_text='스폰서에서 할 수 있는 스폰서 발표의 개수')

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsor_owner')
    name = models.CharField(max_length=255, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    image = SorlImageField(upload_to='sponsor', null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    level = models.ForeignKey(SponsorLevel, null=True,
                              on_delete=models.SET_NULL)
    paid_at = models.DateTimeField(null=True, blank=True)
    ticket_users = models.ForeignKey(User, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='sponsor_ticket_users')

    def __str__(self):
        return f'{self.name}/{self.level}'
