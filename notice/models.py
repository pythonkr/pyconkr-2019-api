from django.db import models


class Notice(models.Model):
    class Meta:
        ordering = ['-published_at', ]

    title = models.CharField(max_length=255, null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True,
                            help_text='공지의 상세를 볼 수 있는 링크입니다. 주로 페이스북 링크가 들어가게 됩니다.')
    active = models.BooleanField(default=True,
                                 help_text='True면 공지사항이 노출됩니다.')
    published_at = models.DateTimeField(null=True, blank=True,
                                        help_text='공지가 노출된 일시입니다.')
