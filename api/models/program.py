from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
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
        return self.presentation_proposal.accepted

    @property
    def submitted(self):
        return self.presentation_proposal.submitted

    def __str__(self):
        return f'{self.owner}/{self.name}'

class PresentationProposal(models.Model):
    presentation = models.OneToOneField(Presentation, related_name='proposal', on_delete=models.CASCADE)
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
    proposal_agreed_at = models.DateTimeField(null=True, blank=True)

    @property
    def name(self):
        return self.presentation.name

    @name.setter
    def name(self, value):
        self.presentation.name = value
        self.presentation.nameKo = value
        self.presentation.nameEn = value

    @property
    def owner(self):
        return self.presentation.owner

    @property
    def background_desc(self):
        return self.presentation.background_desc
    
    @background_desc.setter
    def background_desc(self, value):
        self.presentation.backgroundDesc = value
        self.presentation.backgroundDescKo = value
        self.presentation.backgroundDescEn = value
    
    @property
    def duration(self):
        return self.presentation.duration

    @duration.setter
    def duration(self, value):
        self.presentation.duration = value

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
        if not self.proposal_agreed_at:
            return False
        return True

@receiver(post_save, sender=Presentation)
def create_presentation_proposal(sender, instance, created, **kwargs):
    if created and hasattr(instance, 'proposal'):
        PresentationProposal.objects.create(presentation=instance)

@receiver(post_save, sender=Presentation)
def save_presentation_proposal(sender, instance, **kwargs):
    if hasattr(instance, 'proposal'):
        instance.proposal.save()
    else:
        PresentationProposal.objects.create(presentation=instance)
