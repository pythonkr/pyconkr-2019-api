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
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsor_owner')
    name = models.CharField(max_length=255, null=True, blank=True)
    manager_name = models.CharField(max_length=100, blank=True, default='')
    manager_phone = models.CharField(max_length=100, blank=True, default='')
    manager_secondary_phone = models.CharField(max_length=100, blank=True, default='')
    manager_email = models.EmailField(blank=True, default='')
    level = models.ForeignKey(SponsorLevel, null=True,
                              on_delete=models.SET_NULL, blank=True)
    business_registration_number = models.CharField(max_length=100, blank=True, default='')
    business_registration_image = SorlImageField(upload_to='sponsor_business_registration', blank=True, default='')

    contact_process_required = models.BooleanField(default=False)
    url = models.CharField(max_length=255, null=True, blank=True)
    logo_image = SorlImageField(upload_to='sponsor_logo', null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

    paid_at = models.DateTimeField(null=True, blank=True,
                                   help_text='후원금이 입금된 일시')
    accepted = models.BooleanField(default=False)

    # # one to many로 변경해야함
    # ticket_users = models.ForeignKey(User, on_delete=models.SET_NULL,
    #                                  null=True, blank=True, related_name='sponsor_ticket_users')
    # # one to many로 변경해야함
    # presentations = models.ForeignKey(Presentation, on_delete=models.SET_NULL,
    #                                  null=True, blank=True, related_name='sponsor_presentations')



    def __str__(self):
        return f'{self.name}/{self.level}'
