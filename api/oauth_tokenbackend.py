from django.contrib.auth import get_user_model

UserModel = get_user_model()


class OAuthTokenBackend:
    # TODO: username should be removed, it is only for testing
    def authenticate(self, request, oauth_type='github', oauth_access_token=None, username='amazin2gguni'):
        try:
            # TODO: Should retrive user profile from github/google
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            user = UserModel(username=username)
            user.is_staff = False
            user.is_superuser = False
            user.save()
        return user
