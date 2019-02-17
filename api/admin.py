from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from api.models.oauth_setting import OAuthSetting
from api.models.program import Conference, Presentation
from api.models.program import Place, Category, Difficulty
from api.models.profile import Profile


UserModel = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


admin.site.unregister(UserModel)
admin.site.register(UserModel, UserAdmin)

admin.site.register(OAuthSetting)
admin.site.register(Conference)
admin.site.register(Presentation)
admin.site.register(Place)
admin.site.register(Category)
admin.site.register(Difficulty)
