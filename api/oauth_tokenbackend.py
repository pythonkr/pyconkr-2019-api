from urllib.parse import parse_qs
import requests
from django.contrib.auth import get_user_model
from api.models.oauth_setting import OAuthSetting

UserModel = get_user_model()

OAUTH_TYPE_GITHUB = 'github'
OAUTH_TYPE_GOOGLE = 'google'
OAUTH_TYPE_FACEBOOK = 'facebook'
OAUTH_TYPE_NAVER = 'naver'

OAUTH_TYPES = [OAUTH_TYPE_GITHUB, OAUTH_TYPE_GOOGLE,
               OAUTH_TYPE_FACEBOOK, OAUTH_TYPE_NAVER]


GITHUB_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_PROFILE_URL = 'https://api.github.com/user'
GITHUB_EMAIL_URL = 'https://api.github.com/user/emails'

GITHUB_USERNAME_PREFIX = 'github'


class OAuthTokenBackend:
    def authenticate(self, request, oauth_type, client_id, code):
        try:
            if oauth_type not in OAUTH_TYPES:
                return None
            oauth_setting = self.get_oauth_setting(oauth_type, client_id)
            if oauth_type == OAUTH_TYPE_GITHUB:
                profile_data = self.retrive_github_profile(
                    client_id, oauth_setting.github_client_secret, code)
            # 어떤 OAuth를 통해 인증했는지 구분하기 위해 Prefix를 붙이고
            # 해당 서비스의 계정 Index를 사용해 Username으로 사용합니다
            # e.g, develop_github_3424, localhost_google_25325
            username = f'{oauth_setting.env_name}_{oauth_type}_{profile_data["id"]}'
            user = UserModel.objects.get(
                username=username)
        except UserModel.DoesNotExist:
            user = UserModel(username=username)
            user.email = profile_data['email']
            user.is_staff = False
            user.is_superuser = False
            user.save()

        if not user.profile.name:
            user.profile.name = profile_data['name']
        if not user.profile.avatar_url:
            user.profile.avatar_url = profile_data['avatar_url']
        user.save()
        return user

    def get_oauth_setting(self, oauth_type, client_id):
        params = {
            f'{oauth_type}_client_id': client_id,
            'enable': True
        }
        settings = OAuthSetting.objects.filter(**params)
        if not settings.count():
            raise ValueError(
                f'{oauth_type} client information should be registered by admin(OAuthSetting')
        return settings.last()

    def retrive_github_profile(self, client_id, client_secret, code):
        if not client_id or not client_secret:
            raise ValueError(
                'GitHub client information should be registered by admin(OAuthSetting')
        response = requests.post(GITHUB_ACCESS_TOKEN_URL, data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code
        })
        response.raise_for_status()
        data = parse_qs(response.content.decode('ascii'))
        access_token = data['access_token'][0]
        token_type = data['token_type'][0]
        headers = {
            'Authorization': f'{token_type} {access_token}'
        }
        response = requests.get(GITHUB_PROFILE_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        email = data['email']
        if not email:
            email = self.retrieve_github_email(headers)

        return {
            'id': data['id'],
            'name': data['login'],
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
