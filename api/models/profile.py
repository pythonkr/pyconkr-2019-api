from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField as SorlImageField

# pylint: disable=invalid-name
UserModel = get_user_model()


class Profile(models.Model):
    OAUTH_GITHUB = '1'
    OAUTH_GOOGLE = '2'
    OAUTH_FACEBOOK = '3'
    OAUTH_NAVER = '4'

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    oauth_type = models.CharField(max_length=1,
                                  choices=(
                                      (OAUTH_GITHUB, ('github')),
                                      (OAUTH_GOOGLE, ('google')),
                                      (OAUTH_FACEBOOK, ('facebook')),
                                      (OAUTH_NAVER, ('naver')),
                                  ), default=OAUTH_GITHUB)

    name = models.CharField(max_length=100, blank=True, default='')
    bio = models.TextField(max_length=4000, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    phone = models.CharField(max_length=100, blank=True, default='')
    organization = models.CharField(max_length=100, blank=True, default='')
    nationality = models.CharField(max_length=100, blank=True, default='')
    image = SorlImageField(upload_to='profile', blank=True, default='')
    avatar_url = models.CharField(max_length=500, blank=True, default='')
    blog_url = models.CharField(max_length=200, blank=True, default='')
    github_url = models.CharField(max_length=200, blank=True, default='')
    facebook_url = models.CharField(max_length=200, blank=True, default='')
    twitter_url = models.CharField(max_length=200, blank=True, default='')
    linked_in_url = models.CharField(max_length=200, blank=True, default='')
    instagram_url = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return f'{self.name}({self.email})'


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=UserModel)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)


def get_sns_email(self):
    if not hasattr(self, 'profile'):
        return self.name
    return f'[{self.profile.get_oauth_type_display()}] {self.profile.name} ({self.profile.email})'


get_user_model().add_to_class("__str__", get_sns_email)
