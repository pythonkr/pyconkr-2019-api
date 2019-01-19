from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager

class Sponsor(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100, db_index=True)
    desc = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='sponsor', null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    level = models.ForeignKey(SponsorLevel, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    ticket_users = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

#class SponsorLevel()