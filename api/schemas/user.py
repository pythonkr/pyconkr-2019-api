import os
import graphene
from django.contrib.auth import get_user_model
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.types import Email
from graphql_extensions import exceptions
from graphene_file_upload.scalars import Upload

from api.schemas.common import ImageUrl
from api.models.profile import Profile
from api.models.profile import create_profile_if_not_exists


UserModel = get_user_model()


class OauthTypeNode(graphene.Enum):
    GITHUB = Profile.OAUTH_GITHUB
    GOOGLE = Profile.OAUTH_GOOGLE
    FACEBOOK = Profile.OAUTH_FACEBOOK
    NAVER = Profile.OAUTH_NAVER


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        description = "User Profile"

    oauth_type = graphene.Field(OauthTypeNode)
    image = graphene.Field(ImageUrl)


class UserNode(DjangoObjectType):
    class Meta:
        model = UserModel
        only_fields = ('username', 'email', 'profile', 'is_active',
                       'is_staff', 'is_superuser')
        description = "User information"

    profile = graphene.Field(ProfileNode)


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


class UpdateProfile(graphene.Mutation):
    profile = graphene.Field(ProfileNode)

    class Arguments:
        profile_input = ProfileInput(required=True)

    @login_required
    def mutate(self, info, profile_input):
        profile = create_profile_if_not_exists(info.context.user)
        for k, v in profile_input.items():
            setattr(profile, k, v)
        profile.full_clean()
        profile.save()
        return UpdateProfile(profile=profile)


class UpdateAgreement(graphene.Mutation):
    is_active = graphene.Boolean()
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
        if user.agreement.terms_of_service_agreed_at and user.agreement.privacy_policy_agreed_at:
            user.profile.agreed = True
        user.save()
        return UpdateProfile(is_active=user.is_active, user=user)


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

    @login_required
    def resolve_me(self, info, **kwargs):
        return info.context.user
