from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField as SorlImageField


class SponsorLevel(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    desc = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(default=0)
    ticket_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    name_ko = models.CharField(max_length=255, null=True, blank=True)
    desc_ko = models.TextField(null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    desc_en = models.TextField(null=True, blank=True)
    image = SorlImageField(upload_to='sponsor', null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    level = models.ForeignKey(SponsorLevel, null=True,
                              on_delete=models.SET_NULL)
    paid_at = models.DateField(null=True)
    ticket_users = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_ko
