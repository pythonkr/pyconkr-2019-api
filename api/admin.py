from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from sorl.thumbnail.admin import AdminImageMixin
from api.models.oauth_setting import OAuthSetting
from api.models.program import Conference, Presentation, PresentationProposal
from api.models.program import Place, Category, Difficulty
from api.models.profile import Profile
from api.models.agreement import Agreement
from api.models.sponsor import Sponsor, SponsorLevel

UserModel = get_user_model()


class ProfileInline(AdminImageMixin, admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(UserModel)
admin.site.register(UserModel, UserAdmin)


class AgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'terms_of_service_agreed_at',
                    'privacy_policy_agreed_at')


admin.site.register(Agreement, AgreementAdmin)


class OAuthSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'env_name', 'enable',
                    'github_client_id', 'google_client_id',
                    'facebook_client_id', 'naver_client_id')


admin.site.register(OAuthSetting, OAuthSettingAdmin)


class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'conference_started_at',
                    'conference_finished_at', 'sprint_started_at',
                    'sprint_finished_at', 'tutorial_started_at', 'tutorial_finished_at')


admin.site.register(Conference, ConferenceAdmin)


class PresentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'language', 'category', 'difficulty',
                    'place', 'duration', 'started_at', 'slide_url', 'accepted',)


admin.site.register(Presentation, PresentationAdmin)


class PresentationProposalAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'presentation', 'background_desc', 'duration', 'category', 'detail_desc',
        'is_presented_before', 'place_presented_before', 'presented_slide_url_before', 'comment',
        'proposal_agreed_at', 'submitted', 'accepted')


admin.site.register(PresentationProposal, PresentationProposalAdmin)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Place, PlaceAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'visible')


admin.site.register(Category, CategoryAdmin)


class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Difficulty, DifficultyAdmin)


class SponsorLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'limit',
                    'ticket_count', 'presentation_count')


admin.site.register(SponsorLevel, SponsorLevelAdmin)


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'level', 'paid_at')


admin.site.register(Sponsor, SponsorAdmin)
