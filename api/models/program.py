from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils.managers import InheritanceManager


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

    objects = InheritanceManager()

    name = models.CharField(max_length=255, null=True)
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

    @property
    def accepted(self):
        return self.proposal.accepted

    @property
    def submitted(self):
        return self.proposal.submitted

    def __str__(self):
        return f'{self.owner}/{self.name}'


class PresentationProposal(models.Model):
    presentation = models.OneToOneField(
        Presentation, related_name='proposal', on_delete=models.CASCADE)
    submitted = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    detail_desc = models.TextField(blank=True, default='')
    is_presented_before = models.BooleanField(default=False)
    place_presented_before = models.CharField(
        max_length=255, blank=True, default='')
    presented_slide_url_before = models.CharField(
        max_length=255, blank=True, default='')
    comment = models.TextField(blank=True, default='')
    coc_agreed_at = models.DateTimeField(null=True, blank=True)
    contents_agreed_at = models.DateTimeField(null=True, blank=True)
    etc_agreed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return self.presentation.name

    @name.setter
    def name(self, value):
        self.presentation.name = value
        self.presentation.name_ko = value
        self.presentation.name_en = value

    @property
    def owner(self):
        return self.presentation.owner

    @property
    def background_desc(self):
        return self.presentation.background_desc

    @background_desc.setter
    def background_desc(self, value):
        self.presentation.background_desc = value
        self.presentation.background_desc_ko = value
        self.presentation.background_desc_en = value

    @property
    def duration(self):
        return self.presentation.duration

    @duration.setter
    def duration(self, value):
        self.presentation.duration = value

    @property
    def language(self):
        return self.presentation.language

    @language.setter
    def language(self, value):
        self.presentation.language = value

    @property
    def category(self):
        return self.presentation.category

    @category.setter
    def category(self, value):
        self.presentation.category = value

    @property
    def difficulty(self):
        return self.presentation.difficulty

    @difficulty.setter
    def difficulty(self, value):
        self.presentation.difficulty = value

    def is_agreed_all(self):
        if not self.coc_agreed_at:
            return False
        if not self.contents_agreed_at:
            return False
        if not self.etc_agreed_at:
            return False
        return True


@receiver(post_save, sender=Presentation)
def create_presentation_proposal(sender, instance, created, **kwargs):
    # TODO: 상수가 아닌 다른 방법으로 proposal이 존재하는지 여부를 확인해야 합니다.
    if created and hasattr(instance, 'proposal'):
        PresentationProposal.objects.create(presentation=instance)


@receiver(post_save, sender=Presentation)
def save_presentation_proposal(sender, instance, **kwargs):
    if hasattr(instance, 'proposal'):
        instance.proposal.save()
    else:
        PresentationProposal.objects.create(presentation=instance)
