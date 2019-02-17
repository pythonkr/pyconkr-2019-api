import graphene

from graphene_django import DjangoObjectType
import graphql_jwt
from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.utils import jwt_encode, jwt_payload
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserNode(DjangoObjectType):
    class Meta:
        model = UserModel
        description = "User information"


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


class Mutations(graphene.ObjectType):
    o_auth_token_auth = OAuthTokenAuth.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(graphene.ObjectType):
    profile = graphene.Field(UserNode)

    def resolve_profile(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None
