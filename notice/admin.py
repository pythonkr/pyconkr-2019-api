from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from notice.models import Notice


class NoticeResource(resources.ModelResource):
    class Meta:
        model = Notice


class NoticeAdmin(ImportExportModelAdmin):
    resource_class = NoticeResource
    list_display = ('id', 'title_ko', 'title_en', 'link', 'published_at')


admin.site.register(Notice, NoticeAdmin)
