from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from sorl.thumbnail import ImageField as SorlImageField

# pylint: disable=invalid-name
UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=4000, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    image = SorlImageField(upload_to='profile', blank=True)
    avatar_url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.name}'


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=UserModel)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def create_profile_if_not_exists(user):
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)
        profile.save()
    return profile
