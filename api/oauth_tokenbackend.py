import requests
from django.contrib.auth import get_user_model

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
            name = profile['name']
            email = profile['email']
            avatar_url = profile['avatar_url']
            # 어떤 OAuth를 통해 인증했는지 구분하기 위해 Prefix를 붙입니다.
            # e.g, github_amazingguni, google_amazingguni
            username = f'{oauth_type}_{name}'
            user = UserModel.objects.get(
                username=username)
            if user.email != email:
                user.email = email
                user.save()
        except UserModel.DoesNotExist:
            user = UserModel(username=username, email=email)
            user.is_staff = False
            user.is_superuser = False
            user.save()

        profile = user.profile
        profile.name = name
        profile.email = email
        profile.avatar_url = avatar_url
        profile.save()
        print(user)
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
            'name': data["login"],
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
