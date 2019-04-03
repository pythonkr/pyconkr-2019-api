from django.db import models


class Notice(models.Model):
    title = models.CharField(max_length=50)
    pic_url = models.TextField(blank=True, default='')
    message = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
