from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from model_utils.managers import InheritanceManager


class Conference(models.Model):
    name = models.CharField(max_length=50)
    conference_started_at = models.DateField(null=True, blank=True)
    conference_finished_at = models.DateField(null=True, blank=True)
    sprint_started_at = models.DateField(null=True, blank=True)
    sprint_finished_at = models.DateField(null=True, blank=True)
    tutorial_started_at = models.DateField(null=True, blank=True)
    tutorial_finished_at = models.DateField(null=True, blank=True)

    earlybird_started_at = models.DateTimeField(null=True, blank=True)
    earlybird_finished_at = models.DateTimeField(null=True, blank=True)

    presentation_proposal_started_at = models.DateTimeField(
        null=True, blank=True)
    presentation_proposal_finished_at = models.DateTimeField(
        null=True, blank=True)
    sprint_proposal_started_at = models.DateTimeField(null=True, blank=True)
    sprint_proposal_finished_at = models.DateTimeField(null=True, blank=True)
    tutorial_proposal_started_at = models.DateTimeField(null=True, blank=True)
    tutorial_proposal_finished_at = models.DateTimeField(null=True, blank=True)


class Place(models.Model):
    name = models.CharField(max_length=50, default='', blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Difficulty(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return f'{self.name}'


class Program(models.Model):
    LANGUAGE_ENGLISH = 'E'
    LANGUAGE_KOREAN = 'K'

    objects = InheritanceManager()

    name = models.CharField(max_length=255, null=True, validators=[MinLengthValidator(1)])
    desc = models.TextField(blank=True, default='')
    price = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)

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

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    short_desc = models.TextField(blank=True, default='')
    background_desc = models.TextField(blank=True, default='')
    submitted = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
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

    is_presented_before = models.BooleanField(default=False)
    place_presented_before = models.CharField(
        max_length=255, blank=True, default='')
    presented_slide_url_before = models.CharField(
        max_length=255, blank=True, default='')
    question = models.TextField(blank=True, default='')

    def __str__(self):
        return f'{self.owner}/{self.name}'
