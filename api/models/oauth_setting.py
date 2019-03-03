from django.db import models


class OAuthSetting(models.Model):
    env_name = models.CharField(max_length=50, unique=True)
    enable = models.BooleanField(default=True)

    github_client_id = models.CharField(max_length=100, null=True, blank=True)
    github_client_secret = models.CharField(
        max_length=100, null=True, blank=True)

    google_client_id = models.CharField(max_length=100, null=True, blank=True)
    google_client_secret = models.CharField(
        max_length=100, null=True, blank=True)

    facebook_client_id = models.CharField(
        max_length=100, null=True, blank=True)
    facebook_client_secret = models.CharField(
        max_length=100, null=True, blank=True)

    naver_client_id = models.CharField(max_length=100, null=True, blank=True)
    naver_client_secret = models.CharField(
        max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.env_name}/{self.enable}'
