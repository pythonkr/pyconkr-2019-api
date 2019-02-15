import requests
from django.contrib.auth import get_user_model

# pylint: disable=invalid-name
UserModel = get_user_model()

OAUTH_TYPE_GITHUB = 'github'
OAUTH_TYPE_GOOGLE = 'google'

GITHUB_PROFILE_URL = 'https://api.github.com/user'
GITHUB_EMAIL_URL = 'https://api.github.com/user/emails'

GITHUB_USERNAME_PREFIX = 'github'


class OAuthTokenBackend:
    def authenticate(self, request, oauth_type=OAUTH_TYPE_GITHUB, oauth_access_token=None):
        try:
            if oauth_type != OAUTH_TYPE_GITHUB:
                return None
            profile = self.retrive_github_profile(oauth_access_token)
            username = profile['username']
            email = profile['email']
            user = UserModel.objects.get(username=username, email=email)
        except UserModel.DoesNotExist:
            user = UserModel(username=username, email=email)
            user.is_staff = False
            user.is_superuser = False
            user.save()
        return user

    def retrive_github_profile(self, access_token):
        headers = {
            'Authorization': f'token {access_token}'
        }
        response = requests.get(GITHUB_PROFILE_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        email = data['email']
        if not email:
            email = self.retrieve_github_email(headers)

        return {
            'username': f'{GITHUB_USERNAME_PREFIX}_{data["login"]}',
            'avatar_url': data['avatar_url'],
            'email': email
        }

    def retrieve_github_email(self, headers):
        response = requests.get(GITHUB_EMAIL_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        primary_email = [item['email'] for item in data if item['primary']]
        if not primary_email:
            return None
        return primary_email[0]
