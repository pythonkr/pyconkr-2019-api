import hashlib
import os

from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField as SorlImageField

from api.models.utils import hash_file


class SponsorLevel(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(default=0)
    limit = models.IntegerField(default=0, help_text='스폰서 등급의 구좌수')
    ticket_count = models.IntegerField(default=0, help_text='스폰서에게 제공되는 티켓의 수')
    presentation_count = models.IntegerField(default=0, help_text='스폰서에서 할 수 있는 스폰서 발표의 개수')

    def __str__(self):
        return self.name


def registration_file_upload_to(instance, filename):
    _, ext = os.path.splitext(filename)
    m = hashlib.md5()
    m.update(f'{instance.id}{filename}'.encode('utf-8'))
    return f'sponsor/business_registration/{m.hexdigest()}{ext}'


def logo_image_upload_to(instance, filename):
    _, ext = os.path.splitext(filename)
    m = hashlib.md5()
    m.update(f'{instance.id}{filename}'.encode('utf-8'))
    return f'sponsor/logo/image/{m.hexdigest()}{ext}'


def logo_vector_upload_to(instance, filename):
    _, ext = os.path.splitext(filename)
    m = hashlib.md5()
    m.update(f'{instance.id}{filename}'.encode('utf-8'))
    return f'sponsor/logo/vector/{m.hexdigest()}{ext}'


class Sponsor(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, help_text='후원사를 등록한 유저')
    name = models.CharField(max_length=255, null=True, blank=True, help_text='후원사 이름입니다. 서비스나 회사 이름이 될 수 있습니다.')
    desc = models.TextField(null=True, blank=True, help_text='후원사 설명입니다. 이 설명은 홈페이지에 게시됩니다.')
    manager_name = models.CharField(max_length=100, blank=True, default='', help_text='후원사 담당자의 이름입니다.')
    manager_phone = models.CharField(max_length=100, blank=True, default='', help_text='후원사 담당자의 연락처입니다.')
    manager_secondary_phone = models.CharField(max_length=100, blank=True, default='',
                                               help_text='후원사 담당자 외의 연락이 가능한 연락처입니다.')
    manager_email = models.EmailField(blank=True, default='', help_text='후원사 담당자의 이메일 주소입니다.')
    level = models.ForeignKey(SponsorLevel, null=True,
                              on_delete=models.SET_NULL, blank=True, help_text='후원사 등급입니다.')
    business_registration_number = models.CharField(max_length=100, blank=True, default='',
                                                    help_text='후원사 사업자 등록번호입니다.')
    business_registration_file = models.FileField(
        upload_to=registration_file_upload_to, blank=True, default='', help_text='후원사 사업자 등록증 스캔본입니다.')

    contract_process_required = models.BooleanField(default=False, help_text='후원을 위한 계약 절차가 필요한지 여부입니다')
    url = models.CharField(max_length=255, null=True, blank=True, help_text='후원사 홈페이지 주소입니다. 파이콘 홈페이지에 공개됩니다.')
    logo_image = SorlImageField(upload_to=logo_image_upload_to, null=True, blank=True,
                                help_text='홈페이지에 공개되는 후원사 이미지입니다.')
    logo_vector = SorlImageField(upload_to=logo_vector_upload_to, null=True, blank=True,
                                 help_text='홈페이지에 공개되는 후원사 로고 백터 파일입니다.')

    paid_at = models.DateTimeField(null=True, blank=True,
                                   help_text='후원금이 입금된 일시입니다. 아직 입금되지 않았을 경우 None이 들어갑니다.')
    submitted = models.BooleanField(default=False, help_text='파이콘 준비위원회의 검토 후 후원사의 후원을 받을지 여부를 결정합니다.')
    accepted = models.BooleanField(default=False, help_text='파이콘 준비위원회의 검토 후 후원사의 후원을 받을지 여부를 결정합니다.')

    # # one to many로 변경해야함
    # ticket_users = models.ForeignKey(User, on_delete=models.SET_NULL,
    #                                  null=True, blank=True, related_name='sponsor_ticket_users')
    # # one to many로 변경해야함
    # presentations = models.ForeignKey(Presentation, on_delete=models.SET_NULL,
    #                                  null=True, blank=True, related_name='sponsor_presentations')

    def __str__(self):
        return f'{self.name}/{self.level}'
