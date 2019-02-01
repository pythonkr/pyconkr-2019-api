from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager


class Conference(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} / {self.slug}'


class Difficulty(models.Model):
    name_ko = models.CharField(max_length=100, db_index=True)
    name_en = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return f'{self.name_ko} / {self.name_en}'


class Program(models.Model):
    LANGUAGE_ENGLISH = 'E'
    LANGUAGE_KOREAN = 'K'

    objects = InheritanceManager()

    name_ko = models.CharField(max_length=255, null=True, blank=True)
    desc_ko = models.TextField(null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    desc_en = models.TextField(null=True, blank=True)
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    place = models.ForeignKey(Place, null=True, on_delete=models.SET_NULL)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)
    slide_url = models.CharField(max_length=255, null=True, blank=True)
    pdf_url = models.CharField(max_length=255, null=True, blank=True)
    video_url = models.CharField(max_length=255, null=True, blank=True)
    difficulty = models.ForeignKey(
        Difficulty, null=True, on_delete=models.SET_NULL)
    recordable = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner}/{self.name_ko}'
