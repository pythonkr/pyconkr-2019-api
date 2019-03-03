
import graphene
from django.contrib.auth import authenticate

import graphql_jwt
from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.utils import jwt_encode, jwt_payload


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


class Mutations(graphene.ObjectType):
    o_auth_token_auth = OAuthTokenAuth.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

class Query(graphene.ObjectType):
    pass
