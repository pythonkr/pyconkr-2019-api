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
from api.models.notices import Notice

UserModel = get_user_model()

class ProfileInline(AdminImageMixin, admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class AgreementInline(admin.StackedInline):
    model = Agreement
    can_delete = False
    verbose_name_plural = 'agreement'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, AgreementInline,)


admin.site.unregister(UserModel)
admin.site.register(UserModel, UserAdmin)


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

class PresentationProposalInline(admin.StackedInline):
    model = PresentationProposal
    can_delete = False
    verbose_name_plural = 'proposal'


class PresentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_profile', 'name', 'language', 'category', 'difficulty',
                    'place', 'duration', 'started_at', 'slide_url', 'accepted',)
    inlines = (PresentationProposalInline,)

    def owner_profile(self, obj):
        profile = obj.owner.profile
        return profile if profile else ''

admin.site.register(Presentation, PresentationAdmin)


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
    list_display = ('id', 'name', 'visible', 'price', 'limit',
                    'ticket_count', 'presentation_count', 'booth_info',
                    'program_guide', 'can_provide_goods', 'logo_locations', 'can_recruit')



admin.site.register(SponsorLevel, SponsorLevelAdmin)


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator_profile', 'name', 'level', 'manager_name', 'manager_phone',
                    'manager_email', 'business_registration_number', 'contract_process_required',
                    'url', 'paid_at', 'submitted', 'accepted')

    def creator_profile(self, obj):
        profile = obj.creator.profile
        return profile if profile else ''


admin.site.register(Sponsor, SponsorAdmin)


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')


admin.site.register(Notice, NoticeAdmin)
