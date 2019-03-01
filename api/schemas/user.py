
import graphene
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from graphene_django import DjangoObjectType
import graphql_jwt
from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.utils import jwt_encode, jwt_payload
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.types import Email

from api.models.profile import Profile
from api.models.profile import create_profile_if_not_exists

UserModel = get_user_model()


class UserNode(DjangoObjectType):
    class Meta:
        model = UserModel
        only_fields = ('username', 'email', 'profile')
        description = "User information"

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


class OAuthTokenAuth(graphene.Mutation):
    class Arguments:
        oauth_type = graphene.String(required=True)
        client_id = graphene.String(required=True)
        code = graphene.String(required=True)
        redirect_uri = graphene.String(required=True)

    token = graphene.String()

    def mutate(self, info, oauth_type, client_id, code, redirect_uri):
        try:
            user = authenticate(
                request=info.context,
                oauth_type=oauth_type,
                client_id=client_id,
                code=code,
                redirect_uri=redirect_uri)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e
        if user is None or user.is_anonymous:
            raise JSONWebTokenError(
                'Please, enter valid credentials')
        payload = jwt_payload(user)
        token = jwt_encode(payload)
        return OAuthTokenAuth(token=token)


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


class Mutations(graphene.ObjectType):
    o_auth_token_auth = OAuthTokenAuth.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    update_profile = UpdateProfile.Field()


class Query(graphene.ObjectType):
    profile = graphene.Field(ProfileNode)

    @login_required
    def resolve_profile(self, info, **kwargs):
        return info.context.user.profile
