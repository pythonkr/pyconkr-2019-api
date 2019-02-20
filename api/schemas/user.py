
import graphene
from graphql import GraphQLError
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from graphene_django import DjangoObjectType
import graphql_jwt
from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.utils import jwt_encode, jwt_payload


from api.models.profile import Profile
from api.models.profile import create_profile_if_not_exists

UserModel = get_user_model()


class UserNode(DjangoObjectType):
    class Meta:
        model = UserModel
        only_fields = ('username', 'email', 'profile')
        description = "User information"


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        description = "User Profile"


class OAuthTokenAuth(graphene.Mutation):
    class Arguments:
        oauth_type = graphene.String(required=True)
        client_id = graphene.String(required=True)
        code = graphene.String(required=True)

    token = graphene.String()

    def mutate(self, info, oauth_type, client_id, code):
        from requests.exceptions import HTTPError
        try:
            user = authenticate(
                request=info.context,
                oauth_type=oauth_type,
                client_id=client_id,
                code=code)
        except HTTPError as e:
            raise GraphQLError(e)
        if user is None or user.is_anonymous:
            raise JSONWebTokenError(
                'Please, enter valid credentials')
        payload = jwt_payload(user)
        token = jwt_encode(payload)
        return OAuthTokenAuth(token=token)


class ProfileInput(graphene.InputObjectType):
    name = graphene.String()
    bio = graphene.String()
    phone = graphene.String()
    organization = graphene.String()
    nationality = graphene.String()
    # image = SorlImageField(upload_to='profile', null=True, blank=True)


class UpdateProfile(graphene.Mutation):
    profile = graphene.Field(ProfileNode)

    class Arguments:
        profile_input = ProfileInput(required=True)

    def mutate(self, info, profile_input=None):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You must be logged to PyCon Korea')
        profile = create_profile_if_not_exists(user)

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
    me = graphene.Field(UserNode)

    def resolve_me(self, info):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You must be logged to PyCon Korea')
        return user
