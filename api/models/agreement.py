
from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

# pylint: disable=invalid-name
UserModel = get_user_model()


class Agreement(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    terms_of_service_agreed_at = models.DateTimeField(null=True, blank=True)
    privacy_policy_agreed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_agreed_all(self):
        return self.terms_of_service_agreed_at and self.privacy_policy_agreed_at


@receiver(post_save, sender=UserModel)
def create_user_agreement(sender, instance, created, **kwargs):
    if created:
        Agreement.objects.create(user=instance)


@receiver(post_save, sender=UserModel)
def save_user_agreement(sender, instance, **kwargs):
    if hasattr(instance, 'agreement'):
        instance.agreement.save()
    else:
        Agreement.objects.create(user=instance)


def create_agreement_if_not_exists(user):
    try:
        agreement = Agreement.objects.get(user=user)
    except Agreement.DoesNotExist:
        agreement = Agreement(user=user)
        agreement.save()
    return agreement
