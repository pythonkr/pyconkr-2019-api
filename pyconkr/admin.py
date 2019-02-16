from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from api.models.profile import Profile
from api.models.program import Presentation
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


admin.site.unregister(UserModel)
admin.site.register(UserModel, UserAdmin)

admin.site.register(Presentation)
