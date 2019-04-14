from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from sorl.thumbnail.admin import AdminImageMixin
from api.models.oauth_setting import OAuthSetting
from api.models.schedule import Schedule
from api.models.program import Presentation, PresentationProposal
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


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'conference_start_at',
                    'conference_finish_at', 'tutorial_start_at',
                    'tutorial_finish_at', 'sprint_start_at', 'sprint_finish_at',
                    'earlybird_ticket_start_at', 'earlybird_ticket_finish_at',
                    'conference_ticket_start_at', 'conference_ticket_finish_at')

    fieldsets = (
        (None, {
            'fields': ('name_ko', 'name_en')
        }),
        ('주요 일정', {
            'fields': ('conference_start_at', 'conference_finish_at',
                       'tutorial_start_at', 'tutorial_finish_at',
                       'sprint_start_at', 'sprint_finish_at')
        }),
        ('세션', {
            'fields': (
                'keynote_recommendation_start_at', 'keynote_recommendation_finish_at',
                'keynote_recommendation_announce_at',
                'presentation_proposal_start_at', 'presentation_proposal_finish_at',
                'presentation_review_start_at', 'presentation_review_finish_at',
                'presentation_announce_at')
        }),
        ('튜토리얼', {
            'fields': ('tutorial_proposal_start_at', 'tutorial_proposal_finish_at',
                       'tutorial_proposal_announce_at')
        }),
        ('스프린트', {
            'fields': ('sprint_proposal_start_at', 'sprint_proposal_finish_at',
                       'sprint_proposal_announce_at')
        }),
        ('스폰서', {
            'fields': ('sponsor_proposal_start_at', 'sponsor_proposal_finish_at')
        }),
        ('자원봉사', {
            'fields': ('volunteer_recruiting_start_at', 'volunteer_recruiting_finish_at',
                       'volunteer_announce_at')
        }),
        ('라이트닝토크', {
            'fields': (
                'lightning_talk_proposal_start_at', 'lightning_talk_proposal_finish_at',
                'lightning_talk_announce_at')
        }),
        ('티켓', {
            'fields': ('earlybird_ticket_start_at', 'earlybird_ticket_finish_at',
                       'patron_ticket_start_at', 'patron_ticket_finish_at',
                       'conference_ticket_start_at', 'conference_ticket_finish_at',
                       'tutorial_ticket_start_at', 'tutorial_ticket_finish_at',
                       'sprint_ticket_start_at', 'sprint_ticket_finish_at',
                       'babycare_ticket_start_at', 'babycare_ticket_finish_at',
                       'youngcoder_ticket_start_at', 'youngcoder_ticket_finish_at')
        }),
        ('재정지원', {
            'fields': ('financial_aid_start_at', 'financial_aid_finish_at',
                       'financial_aid_announce_at')
        })
    )


admin.site.register(Schedule, ScheduleAdmin)


class PresentationProposalInline(admin.StackedInline):
    model = PresentationProposal
    can_delete = False
    verbose_name_plural = 'proposal'


class PresentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_profile', 'name', 'language', 'category', 'difficulty',
                    'place', 'duration', 'started_at', 'slide_url', 'accepted',)
    inlines = (PresentationProposalInline,)

    def owner_profile(self, obj):
        return Profile.objects.get_or_create(user = obj.owner)


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
    list_display = ('id', 'name', 'visible', 'price', 'limit', 'current_remaining_number',
                    'ticket_count', 'presentation_count', 'booth_info',
                    'program_guide', 'can_provide_goods', 'logo_locations', 'can_recruit')


admin.site.register(SponsorLevel, SponsorLevelAdmin)


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator_profile', 'name', 'level', 'manager_name', 'manager_phone',
                    'manager_email', 'business_registration_number', 'contract_process_required',
                    'url', 'submitted', 'accepted', 'paid_at')
    actions = ['accept', 'reject']

    def creator_profile(self, obj):
        return Profile.objects.get_or_create(user=obj.creator)

    def accept(self, request, queryset):
        queryset.update(accepted=True)

    def reject(self, request, queryset):
        queryset.update(accepted=False)

    accept.short_description = "Accept sponsorship"
    reject.short_description = "Reject sponsorship"


admin.site.register(Sponsor, SponsorAdmin)


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')


admin.site.register(Notice, NoticeAdmin)
