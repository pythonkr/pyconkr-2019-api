from django.contrib import admin

from notice.models import Notice


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ko', 'title_en', 'link', 'published_at')


admin.site.register(Notice, NoticeAdmin)
