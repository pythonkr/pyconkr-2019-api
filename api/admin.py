import math
from datetime import timedelta, timezone

from constance import config
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export import fields
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from sorl.thumbnail.admin import AdminImageMixin

from api.models import CFPReview
from api.models.agreement import Agreement
from api.models.oauth_setting import OAuthSetting
from api.models.profile import Profile
from api.models.program import Place, Category, Difficulty, Sprint, Tutorial
from api.models.program import Presentation
from api.models.schedule import Schedule
from api.models.sponsor import Sponsor, SponsorLevel
from ticket.models import TicketProduct

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
    list_filter = (
        ('profile__is_volunteer', admin.BooleanFieldListFilter),
        ('profile__is_organizer', admin.BooleanFieldListFilter),
    )


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
    autocomplete_fields = ['owner', 'secondary_owner']
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


class PlaceResource(resources.ModelResource):
    class Meta:
        model = Place


class PlaceAdmin(ImportExportModelAdmin):
    resource_class = PlaceResource
    list_display = ('id', 'name')


admin.site.register(Place, PlaceAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'visible')


admin.site.register(Category, CategoryAdmin)


class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Difficulty, DifficultyAdmin)


class TutorialResource(resources.ModelResource):
    class Meta:
        model = Tutorial


class TutorialAdmin(ImportExportModelAdmin):
    resource_class = TutorialResource
    actions = ('accept', 'update_ticket_product')
    autocomplete_fields = ['owner', ]
    list_display = ('id', 'owner', 'name', 'num_of_participants', 'language', 'difficulty',
                    'place', 'started_at', 'finished_at', 'submitted', 'accepted',)
    list_filter = (
        'difficulty',
        'language',
        ('submitted', admin.BooleanFieldListFilter),
        ('accepted', admin.BooleanFieldListFilter),
        ('place', admin.RelatedOnlyFieldListFilter),
    )

    def accept(self, request, queryset):
        queryset.update(submitted=True, accepted=True)

    def update_ticket_product(self, request, queryset):
        for tutorial in queryset:
            if not tutorial.accepted:
                continue
            if not tutorial.ticket_product:
                tutorial.ticket_product = TicketProduct.objects.create()
                tutorial.save()
            product = tutorial.ticket_product
            product.type = TicketProduct.TYPE_TUTORIAL
            product.is_unique_in_type = False
            product.name = tutorial.name
            product.name_en = tutorial.name_en
            product.name_ko = tutorial.name_ko
            product.owner = tutorial.owner
            product.desc_en = 'You can pick up your name tag by presenting this ticket ' \
                              'at the venue on the day of the tutorial.'
            product.desc_ko = tutorial.desc_ko
            product.start_at = tutorial.started_at
            product.finish_at = tutorial.finished_at
            period_delta = tutorial.finished_at - tutorial.started_at
            period_hour = math.ceil(period_delta.seconds / 60 / 60)
            product.price = config.TUTORIAL_PRICE_PER_HOUR * period_hour
            cancelable_date = tutorial.started_at - timedelta(days=2)
            KST = timezone(timedelta(hours=9))
            cancelable_date = cancelable_date.replace(hour=18, minute=0, second=0,
                                                      microsecond=0, tzinfo=KST)
            product.cancelable_date = cancelable_date
            product.warning_ko = f'취소, 환불 기한: {cancelable_date.year}년 ' \
                f'{cancelable_date.month}월 {cancelable_date.day}일 오후 6시까지'
            product.warning_en = f'Refund due date: {cancelable_date.year}-' \
                f'{cancelable_date.month}-{cancelable_date.day} 6pm'

            product.total = tutorial.num_of_participants

            schedule = Schedule.objects.last()
            if schedule:
                product.ticket_open_at = schedule.tutorial_ticket_start_at
                product.ticket_close_at = schedule.tutorial_ticket_finish_at
            product.save()
        self.message_user(request, message='제품 생성이 완료되었습니다.')

    update_ticket_product.short_description = "선택한 프로그램으로 Product 생성"


admin.site.register(Tutorial, TutorialAdmin)


class SprintResource(resources.ModelResource):
    class Meta:
        model = Sprint


class SprintAdmin(ImportExportModelAdmin):
    resource_class = SprintResource
    actions = ('accept', 'update_ticket_product',)
    autocomplete_fields = ['owner', ]
    list_display = ('id', 'owner_profile', 'name', 'language', 'programming_language',
                    'place', 'started_at', 'finished_at', 'submitted',
                    'accepted',)
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

    def update_ticket_product(self, request, queryset):
        for sprint in queryset:
            if not sprint.accepted:
                continue
            if not sprint.ticket_product:
                sprint.ticket_product = TicketProduct.objects.create()
                sprint.save()
            product = sprint.ticket_product
            product.type = TicketProduct.TYPE_SPRINT
            product.is_unique_in_type = False
            product.name = sprint.name
            product.name_en = sprint.name_en
            product.name_ko = sprint.name_ko
            product.owner = sprint.owner
            product.desc_en = 'You can pick up your name tag by presenting this ticket ' \
                              'at the venue on the day of the sprint.'
            product.desc_ko = '스프린트 당일 행사장에서 본 티켓을 제시하시면 명찰을 수령하실 수 있습니다.'
            product.start_at = sprint.started_at
            product.finish_at = sprint.finished_at
            product.price = 0
            cancelable_date = sprint.started_at - timedelta(days=2)
            KST = timezone(timedelta(hours=9))
            cancelable_date = cancelable_date.replace(hour=18, minute=0, second=0,
                                                      microsecond=0, tzinfo=KST)
            product.cancelable_date = cancelable_date
            product.warning_ko = f'취소, 환불 기한: {cancelable_date.year}년 ' \
                f'{cancelable_date.month}월 {cancelable_date.day}일 오후 6시까지'
            product.warning_en = f'Refund due date: {cancelable_date.year}-' \
                f'{cancelable_date.month}-{cancelable_date.day} 6pm'

            product.total = 100

            schedule = Schedule.objects.last()
            if schedule:
                product.ticket_open_at = schedule.sprint_ticket_start_at
                product.ticket_close_at = schedule.sprint_ticket_finish_at
            product.save()
        self.message_user(request, message='제품 생성이 완료되었습니다.')

    update_ticket_product.short_description = "선택한 프로그램으로 Product 생성"


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
