from django.db import models


class OAuthSetting(models.Model):
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
