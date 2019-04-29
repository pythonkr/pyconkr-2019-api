from django.contrib.auth.models import User
from django.db import models


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
    owner = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
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
    submitted = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner}/{self.name}'
