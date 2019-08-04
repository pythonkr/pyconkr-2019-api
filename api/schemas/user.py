import os

import graphene
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.exceptions import GraphQLError
from graphql_extensions.types import Email

from api.models.agreement import Agreement
from api.models.profile import Profile
from api.schemas.common import SeoulDateTime, ImageUrl
from ticket.models import TicketProduct, Ticket

UserModel = get_user_model()


class OauthTypeNode(graphene.Enum):
    GITHUB = Profile.OAUTH_GITHUB
    GOOGLE = Profile.OAUTH_GOOGLE
    FACEBOOK = Profile.OAUTH_FACEBOOK
    NAVER = Profile.OAUTH_NAVER


class AgreementNode(DjangoObjectType):
    class Meta:
        model = Agreement

    terms_of_service_agreed_at = graphene.Field(SeoulDateTime)
    privacy_policy_agreed_at = graphene.Field(SeoulDateTime)
    created_at = graphene.Field(SeoulDateTime)
    updated_at = graphene.Field(SeoulDateTime)


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        description = 'User Profile'

    oauth_type = graphene.Field(OauthTypeNode)
    image = graphene.String()
    is_patron = graphene.Boolean(source='is_patron')
    is_open_reviewer = graphene.Boolean(source='is_open_reviewer')
    is_speaker = graphene.Boolean(source='is_speaker')
    is_sprint_owner = graphene.Boolean(source='is_sprint_owner')
    is_tutorial_owner = graphene.Boolean(source='is_tutorial_owner')

    def resolve_image(self, info):
        if self.image.name:
            return self.image.url
        return self.avatar_url


class PatronNode(DjangoObjectType):
    class Meta:
        model = Profile
        only_fields = ('id', 'name', 'name_ko', 'name_en', 'bio', 'bio_ko', 'bio_en',
                       'organization', 'image', 'avatar_url')
        description = 'Patron profiles'

    image = graphene.String()

    def resolve_image(self, info):
        if self.image.name:
            return self.image.url
        return self.avatar_url


class UserNode(DjangoObjectType):
    class Meta:
        model = UserModel
        only_fields = ('username', 'email', 'profile', 'is_active',
                       'is_staff', 'is_superuser')
        description = "User information"

    profile = graphene.Field(ProfileNode)
    is_agreed = graphene.Boolean()

    def resolve_is_agreed(self, info):
        if not self.agreement:
            return False
        return self.agreement.is_agreed_all()


class ProfileInput(graphene.InputObjectType):
    name = graphene.String()
    name_ko = graphene.String()
    name_en = graphene.String()
    bio = graphene.String()
    bio_ko = graphene.String()
    bio_en = graphene.String()
    phone = graphene.String()
    email = Email()
    organization = graphene.String()
    nationality = graphene.String()
    signature = graphene.String()
    blog_url = graphene.String()
    github_url = graphene.String()
    facebook_url = graphene.String()
    twitter_url = graphene.String()
    linkedin_url = graphene.String()
    instagram_url = graphene.String()


class UpdateProfile(graphene.Mutation):
    profile = graphene.Field(ProfileNode)

    class Arguments:
        data = ProfileInput(required=True)

    @login_required
    def mutate(self, info, data):
        profile = info.context.user.profile
        for k, v in data.items():
            setattr(profile, k, v)
        profile.full_clean()
        profile.save()
        return UpdateProfile(profile=profile)


class UpdateAgreement(graphene.Mutation):
    is_agreed_all = graphene.Boolean()
    user = graphene.Field(UserNode)

    class Arguments:
        is_terms_of_service = graphene.Boolean()
        is_privacy_policy = graphene.Boolean()

    @login_required
    def mutate(self, info, is_terms_of_service=False, is_privacy_policy=False):
        user = info.context.user
        if is_terms_of_service:
            user.agreement.terms_of_service_agreed_at = timezone.now()
        if is_privacy_policy:
            user.agreement.privacy_policy_agreed_at = timezone.now()
        user.save()
        return UpdateAgreement(is_agreed_all=user.agreement.is_agreed_all(),
                               user=user)


class UploadProfileImage(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()
    image = graphene.Field(ImageUrl)

    @login_required
    def mutate(self, info, file, **kwargs):
        profile = info.context.user.profile
        if profile.image.name:
            profile.image.delete()
        extension = os.path.splitext(file.name)[1]
        profile.image.save(f'{profile.id}{extension}', file)
        return UploadProfileImage(success=True, image=profile.image)


class Mutations(graphene.ObjectType):
    update_profile = UpdateProfile.Field()
    upload_profile_image = UploadProfileImage.Field()
    update_agreement = UpdateAgreement.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserNode)
    patrons = graphene.List(PatronNode)
    volunteers = graphene.List(PatronNode)
    organizers = graphene.List(PatronNode)

    @login_required
    def resolve_me(self, info, **kwargs):
        user = info.context.user
        Profile.objects.get_or_create(user=user)
        return user

    def resolve_patrons(self, info, **kwargs):
        try:
            patron_product = TicketProduct.objects.get(type=TicketProduct.TYPE_CONFERENCE, is_editable_price=True,
                                                       active=True)
            tickets = Ticket.objects.filter(
                product=patron_product, status=Ticket.STATUS_PAID).order_by('-amount', 'paid_at')
            return [ticket.owner.profile for ticket in tickets]
        except TicketProduct.DoesNotExist:
            raise GraphQLError(_('개인후원 제품이 없습니다. 관리자에게 문의해주세요.'))

    def resolve_volunteers(self, info):
        return Profile.objects.filter(is_volunteer=True)

    def resolve_organizers(self, info):
        return Profile.objects.filter(is_organizer=True)
