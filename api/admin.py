from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export import fields
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from sorl.thumbnail.admin import AdminImageMixin

from api.models import CFPReview
from api.models.agreement import Agreement
from api.models.notices import Notice
from api.models.oauth_setting import OAuthSetting
from api.models.profile import Profile
from api.models.program import Place, Category, Difficulty, Sprint
from api.models.program import Presentation
from api.models.schedule import Schedule
from api.models.sponsor import Sponsor, SponsorLevel

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
    search_fields = ['email', 'profile__email', 'profile__name']


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
                       'childcare_ticket_start_at', 'childcare_ticket_finish_at',
                       'youngcoder_ticket_start_at', 'youngcoder_ticket_finish_at')
        }),
        ('재정지원', {
            'fields': ('financial_aid_start_at', 'financial_aid_finish_at',
                       'financial_aid_announce_at')
        })
    )


admin.site.register(Schedule, ScheduleAdmin)


class PresentationResource(resources.ModelResource):
    submitted = fields.Field(column_name='submitted', attribute='submitted')
    accepted = fields.Field(column_name='accepted', attribute='accepted')
    detail_desc = fields.Field(column_name='detail_desc',
                               attribute='detail_desc')
    is_presented_before = fields.Field(column_name='is_presented_before',
                                       attribute='is_presented_before')
    place_presented_before = fields.Field(column_name='place_presented_before',
                                          attribute='place_presented_before')
    presented_slide_url_before = fields.Field(column_name='presented_slide_url_before',
                                              attribute='presented_slide_url_before')
    created_at = fields.Field(column_name='created_at', attribute='created_at')
    updated_at = fields.Field(column_name='updated_at', attribute='updated_at')
    owner = fields.Field(column_name='owner', attribute='owner__profile__name')
    category = fields.Field(column_name='category', attribute='category__name')
    difficulty = fields.Field(column_name='category', attribute='difficulty__name')

    class Meta:
        model = Presentation


class PresentationAdmin(ImportExportModelAdmin):
    resource_class = PresentationResource
    actions = ('accept',)
    list_display = ('id', 'owner_profile', 'name', 'language', 'category', 'difficulty',
                    'place', 'duration', 'started_at', 'slide_url', 'submitted', 'accepted',)
    autocomplete_fields = ['secondary_owner']
    list_filter = (
        'language',
        ('submitted', admin.BooleanFieldListFilter),
        ('accepted', admin.BooleanFieldListFilter),
        ('category', admin.RelatedOnlyFieldListFilter),
        ('difficulty', admin.RelatedOnlyFieldListFilter),
        ('place', admin.RelatedOnlyFieldListFilter),
        'duration'
    )

    def owner_profile(self, obj):
        if obj.owner:
            profile, _ = Profile.objects.get_or_create(user=obj.owner)
            return profile
        return ''

    def accept(self, request, queryset):
        queryset.update(accepted=True)


admin.site.register(Presentation, PresentationAdmin)


class CFPReviewResource(resources.ModelResource):
    reviewer = fields.Field(column_name='reviewer', attribute='owner__profile__name')
    owner = fields.Field(column_name='owner', attribute='owner__profile__name')
    owner_email = fields.Field(column_name='owner_email', attribute='owner__profile__email')
    presentation = fields.Field(column_name='presentation', attribute='presentation__name')
    presentation_owner = fields.Field(column_name='presentation_owner', attribute='presentation__owner__profile__name')
    category = fields.Field(column_name='category', attribute='presentation__category__name')
    difficulty = fields.Field(column_name='difficulty', attribute='presentation__difficulty__name')
    duration = fields.Field(column_name='duration', attribute='presentation__duration')
    detail_desc = fields.Field(column_name='detail_desc', attribute='presentation__detail_desc')
    background_desc = fields.Field(column_name='background_desc', attribute='presentation__background_desc')

    class Meta:
        model = CFPReview


class CFPReviewAdmin(ImportExportModelAdmin):
    resource_class = CFPReviewResource
    list_display = ('owner_profile', 'presentation', 'submitted', 'submitted_at', 'comment')
    list_filter = (
        ('owner', admin.RelatedOnlyFieldListFilter),
        ('submitted', admin.BooleanFieldListFilter),
        ('presentation', admin.RelatedOnlyFieldListFilter),
    )

    def owner_profile(self, obj):
        if obj.owner:
            profile, _ = Profile.objects.get_or_create(user=obj.owner)
            return profile
        return ''


admin.site.register(CFPReview, CFPReviewAdmin)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Place, PlaceAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'visible')


admin.site.register(Category, CategoryAdmin)


class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Difficulty, DifficultyAdmin)


class SprintResource(resources.ModelResource):
    owner = fields.Field(column_name='owner', attribute='owner__profile__name')

    class Meta:
        model = Sprint


class SprintAdmin(ImportExportModelAdmin):
    resource_class = SprintResource
    actions = ('accept',)
    list_display = ('id', 'owner_profile', 'name', 'language',
                    'place', 'started_at', 'finished_at', 'submitted', 'accepted',)
    list_filter = (
        'language',
        ('submitted', admin.BooleanFieldListFilter),
        ('accepted', admin.BooleanFieldListFilter),
        ('place', admin.RelatedOnlyFieldListFilter),
    )

    def owner_profile(self, obj):
        if obj.owner:
            profile, _ = Profile.objects.get_or_create(user=obj.owner)
            return profile
        return ''

    def accept(self, request, queryset):
        queryset.update(submitted=True, accepted=True)


admin.site.register(Sprint, SprintAdmin)


class SponsorLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'visible', 'price', 'limit', 'current_remaining_number',
                    'accepted_count', 'ticket_count', 'presentation_count', 'booth_info',
                    'program_guide', 'can_provide_goods', 'logo_locations', 'can_recruit')


admin.site.register(SponsorLevel, SponsorLevelAdmin)


class SponsorResource(resources.ModelResource):
    class Meta:
        model = Sponsor

    creator = fields.Field(column_name='creator', attribute='creator__profile__name')
    level = fields.Field(column_name='level', attribute='level__name')


class SponsorAdmin(ImportExportModelAdmin):
    resource_class = SponsorResource
    list_display = ('id', 'creator_profile', 'name', 'level', 'manager_name',
                    'manager_email', 'business_registration_number',
                    'url', 'submitted', 'accepted', 'paid_at')
    actions = ['accept', 'reject']

    list_filter = (
        ('submitted', admin.BooleanFieldListFilter),
        ('accepted', admin.BooleanFieldListFilter),
        'paid_at',
        ('level', admin.RelatedOnlyFieldListFilter),
    )

    def creator_profile(self, obj):
        if obj.creator:
            profile, _ = Profile.objects.get_or_create(user=obj.creator)
            return profile
        return ''

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
