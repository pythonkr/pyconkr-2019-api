import hashlib

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from sorl.thumbnail import ImageField as SorlImageField
from .utils import notify_slack


class SponsorLevel(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    visible = models.BooleanField(default=True)
    price = models.IntegerField(default=0)
    limit = models.IntegerField(default=0,
                                help_text='후원사 등급 별 구좌수')
    ticket_count = models.IntegerField(default=0,
                                       help_text='후원사에게 제공되는 티켓 수')
    presentation_count = models.IntegerField(default=0,
                                             help_text='후원사에게 제공되는 스폰서 발표 수')
    booth_info = models.CharField(max_length=100, blank=True, default='',
                                  help_text='후원사에게 제공되는 부스 정보')
    program_guide = models.CharField(max_length=100, blank=True, default='',
                                     help_text='프로그램 가이드에 후원사 소개가 수록되는 것에 대한 정보')
    can_provide_goods = models.BooleanField(default=False,
                                            help_text='후원사 증정품을 파이콘 참가자에게 제공할 수 있는지 여부')
    open_lunch = models.CharField(max_length=100, blank=True, default='',
                                  help_text='열린 점심 정보, 제공되지 않을 경우 공백')
    logo_locations = models.TextField(null=True, blank=True,
                                      help_text='로고가 노출되는 위치에 대한 설명입니다.')
    can_recruit = models.BooleanField(default=True,
                                      help_text='후원사 채용 공고를 할 수 있는지 여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def current_remaining_number(self):
        return self.limit - Sponsor.objects.filter(
            level=self, submitted=True, accepted=True, paid_at__isnull=False).count()

    @property
    def current_remaining_number_compare_with_accepted(self):
        accepted_cnt = Sponsor.objects.filter(level=self, submitted=True, accepted=True).count()
        return self.limit - accepted_cnt

    def __str__(self):
        return self.name


def registration_file_upload_to(instance, filename):
    m = hashlib.md5()
    m.update(f'{instance.id}{filename}'.encode('utf-8'))
    return f'sponsor/business_registration/{m.hexdigest()}/{filename}'


def logo_image_upload_to(instance, filename):
    m = hashlib.md5()
    m.update(f'{instance.id}{filename}'.encode('utf-8'))
    return f'sponsor/logo/image/{m.hexdigest()}/{filename}'


def logo_vector_upload_to(instance, filename):
    m = hashlib.md5()
    m.update(f'{instance.id}{filename}'.encode('utf-8'))
    return f'sponsor/logo/vector/{m.hexdigest()}/{filename}'


class Sponsor(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                help_text='후원사를 등록한 유저')
    name = models.CharField(max_length=255, null=True, blank=True,
                            help_text='후원사 이름입니다. 서비스나 회사 이름이 될 수 있습니다.')
    level = models.ForeignKey(SponsorLevel, null=True,
                              on_delete=models.SET_NULL, blank=True,
                              help_text='후원사 등급입니다.')
    desc = models.TextField(null=True, blank=True,
                            help_text='후원사 설명입니다. 이 설명은 홈페이지에 게시됩니다.')
    manager_name = models.CharField(max_length=100, blank=True, default='',
                                    help_text='후원사 담당자의 이름입니다.')
    manager_email = models.CharField(max_length=100, blank=True, default='',
                                     help_text='후원사 담당자의 이메일 주소입니다.')
    business_registration_number = models.CharField(max_length=100, blank=True, default='',
                                                    help_text='후원사 사업자 등록번호입니다.')
    business_registration_file = models.FileField(
        upload_to=registration_file_upload_to, blank=True, default='',
        help_text='후원사 사업자 등록증 스캔본입니다.')

    url = models.CharField(max_length=255, null=True, blank=True,
                           help_text='후원사 홈페이지 주소입니다. 파이콘 홈페이지에 공개됩니다.')
    logo_image = SorlImageField(upload_to=logo_image_upload_to, null=True, blank=True,
                                help_text='홈페이지에 공개되는 후원사 이미지입니다.')
    logo_vector = SorlImageField(upload_to=logo_vector_upload_to, null=True, blank=True,
                                 help_text='홈페이지에 공개되는 후원사 로고 백터 파일입니다.')
    paid_at = models.DateTimeField(null=True, blank=True,
                                   help_text='후원금이 입금된 일시입니다. 아직 입금되지 않았을 경우 None이 들어갑니다.')
    submitted = models.BooleanField(default=False,
                                    help_text='사용자가 제출했는지 여부를 저장합니다..')
    accepted = models.BooleanField(default=False,
                                   help_text='파이콘 준비위원회의 검토 후 후원사의 후원을 받을지 여부를 결정합니다.')

    # # one to many로 변경해야함
    # ticket_users = models.ForeignKey(User, on_delete=models.SET_NULL,
    #                                  null=True, blank=True, related_name='sponsor_ticket_users')
    # # one to many로 변경해야함
    # presentations = models.ForeignKey(Presentation, on_delete=models.SET_NULL,
    #                                  null=True, blank=True, related_name='sponsor_presentations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}/{self.level}'


@receiver(post_save, sender=Sponsor)
def send_slack_notification_sponsor_created(sender, instance, created, raw, using, update_fields,
                                            **kwargs):
    def check_attr(obj, name):
        if hasattr(obj, name) and getattr(obj, name) not in [None, ""]:
            return True
        return False

    # name and level should be created
    if check_attr(instance, 'name') and check_attr(instance, 'level'):
        to_channel = "#sponsor"
        message = "%s sponsor requested with %s level" % (instance.name, instance.level)
        notify_slack(to_channel, message)
