from django.contrib.auth import get_user_model
from django.db import models

from ticket.models import TicketProduct

UserModel = get_user_model()


class Place(models.Model):
    name = models.CharField(max_length=50, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Difficulty(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Program(models.Model):
    LANGUAGE_ENGLISH = 'E'
    LANGUAGE_KOREAN = 'K'

    name = models.CharField(max_length=255, null=True)
    desc = models.TextField(blank=True, default='')
    visible = models.BooleanField(default=True)

    language = models.CharField(max_length=1,
                                choices=(
                                    (LANGUAGE_ENGLISH, ('English')),
                                    (LANGUAGE_KOREAN, ('Korean')),
                                ), default=LANGUAGE_KOREAN)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Presentation(Program):
    DURATION_SHORT = 'S'
    DURATION_LONG = 'L'
    is_keynote = models.BooleanField(default=False, help_text='키노트 스피커인 경우 TRUE로 설정합니다.')
    owner = models.OneToOneField(UserModel, null=True, on_delete=models.SET_NULL)
    secondary_owner = models.ForeignKey(UserModel, blank=True, null=True, on_delete=models.SET_NULL,
                                        related_name='secondary_owner_of')
    background_desc = models.TextField(blank=True, default='')

    place = models.ForeignKey(
        Place, blank=True, null=True, on_delete=models.SET_NULL)
    duration = models.CharField(max_length=1,
                                choices=(
                                    (DURATION_SHORT, ('25')),
                                    (DURATION_LONG, ('40')),
                                ), default=DURATION_SHORT)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    difficulty = models.ForeignKey(
        Difficulty, null=True, blank=True, on_delete=models.SET_NULL)
    slide_url = models.CharField(max_length=255, blank=True, default='')
    pdf_url = models.CharField(max_length=255, blank=True, default='')
    video_url = models.CharField(max_length=255, blank=True, default='')
    recordable = models.BooleanField(default=True)

    detail_desc = models.TextField(blank=True, default='')
    is_presented_before = models.BooleanField(default=False)
    place_presented_before = models.CharField(
        max_length=255, blank=True, default='')
    presented_slide_url_before = models.CharField(
        max_length=255, blank=True, default='')
    comment = models.TextField(blank=True, default='')
    submitted = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner}/{self.name}'


class Sprint(Program):
    num_of_participants = models.IntegerField(default=0,
                                              help_text='수강 적절 인원 수 입니다.')
    owner = models.ForeignKey(UserModel, blank=True, null=True, on_delete=models.SET_NULL)
    opensource_desc = models.TextField(blank=True, default='')
    opensource_url = models.CharField(
        max_length=255, blank=True, default='')
    place = models.ForeignKey(
        Place, blank=True, null=True, on_delete=models.SET_NULL)
    ticket_product = models.ForeignKey(
        TicketProduct, blank=True, null=True, on_delete=models.SET_NULL)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    submitted = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner}/{self.name}'


class Tutorial(Program):
    num_of_participants = models.IntegerField(default=0,
                                              help_text='수강 적절 인원 수 입니다.')
    owner = models.ForeignKey(UserModel, blank=True, null=True, on_delete=models.SET_NULL)
    difficulty = models.ForeignKey(
        Difficulty, null=True, blank=True, on_delete=models.SET_NULL)
    place = models.ForeignKey(
        Place, blank=True, null=True, on_delete=models.SET_NULL)
    ticket_product = models.ForeignKey(
        TicketProduct, blank=True, null=True, on_delete=models.SET_NULL)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    submitted = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner}/{self.name}'
