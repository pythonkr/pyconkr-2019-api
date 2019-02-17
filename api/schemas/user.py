
import graphene
from graphql import GraphQLError
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from graphene_django import DjangoObjectType
import graphql_jwt
from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.utils import jwt_encode, jwt_payload


from api.models.profile import Profile

UserModel = get_user_model()


class UserNode(DjangoObjectType):
    class Meta:
        model = UserModel
        description = "User information"


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        description = "User Profile"


class OAuthTokenAuth(graphene.Mutation):
    class Arguments:
        oauth_type = graphene.String()
        oauth_access_token = graphene.String()

    token = graphene.String()

    def mutate(self, info, oauth_type=None, oauth_access_token=None):
        user = authenticate(
            request=info.context,
            oauth_type=oauth_type,
            oauth_access_token=oauth_access_token)
        if user is None:
            raise JSONWebTokenError(
                'Please, enter valid credentials')
        payload = jwt_payload(user)
        token = jwt_encode(payload)
        return OAuthTokenAuth(token=token)


class ProfileInput(graphene.InputObjectType):
    name = graphene.String(required=False)
    bio = graphene.String(required=False)
    phone = graphene.String(required=False)
    organization = graphene.String(required=False)
    nationality = graphene.String(required=False)
    # image = SorlImageField(upload_to='profile', null=True, blank=True)


class UpdateProfile(graphene.Mutation):
    profile = graphene.Field(ProfileNode)

    class Arguments:
        profile_data = ProfileInput(required=True)

    def mutate(self, info, profile_data=None):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You must be logged to PyCon Korea')

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile(user=user)
            profile.save()

        for k, v in profile_data.items():
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
    profile = graphene.Field(UserNode)

    def resolve_profile(self, info):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You must be logged to PyCon Korea')
        return user
