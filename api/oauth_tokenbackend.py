from requests_oauthlib import OAuth2Session
from django.contrib.auth import get_user_model
from api.models.profile import Profile
from api.models.oauth_setting import OAuthSetting

UserModel = get_user_model()

OAUTH_TYPE_GITHUB = 'github'
OAUTH_TYPE_GOOGLE = 'google'
OAUTH_TYPE_FACEBOOK = 'facebook'
OAUTH_TYPE_NAVER = 'naver'

OAUTH_TYPES = [OAUTH_TYPE_GITHUB, OAUTH_TYPE_GOOGLE,
               OAUTH_TYPE_FACEBOOK, OAUTH_TYPE_NAVER]

REDIRECT_URI = 'http://localhost:3000'

GITHUB_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_PROFILE_URL = 'https://api.github.com/user'
GITHUB_EMAIL_URL = 'https://api.github.com/user/emails'

GOOGLE_ACCESS_TOKEN_URL = "https://www.googleapis.com/oauth2/v4/token"
GOOGLE_PROFILE_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'
GOOGLE_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile']

FACEBOOK_ACCESS_TOKEN_URL = "https://graph.facebook.com/v3.2/oauth/access_token"
FACEBOOK_PROFILE_URL = 'https://graph.facebook.com/me?fields=id,email,name,picture'

NAVER_ACCESS_TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
NAVER_PROFILE_URL = 'https://openapi.naver.com/v1/nid/me'


class OAuthTokenBackend:
    def authenticate(self, request, oauth_type, client_id, code, redirect_uri):
        try:
            if oauth_type not in OAUTH_TYPES:
                return None
            oauth_setting = self.get_oauth_setting(oauth_type, client_id)

            if oauth_type == OAUTH_TYPE_GITHUB:
                profile_data = self.retrieve_github_profile(
                    client_id, oauth_setting.github_client_secret, code, redirect_uri)
            elif oauth_type == OAUTH_TYPE_GOOGLE:
                profile_data = self.retrieve_google_profile(
                    client_id, oauth_setting.google_client_secret, code, redirect_uri)
            elif oauth_type == OAUTH_TYPE_FACEBOOK:
                profile_data = self.retrieve_facebook_profile(
                    client_id, oauth_setting.facebook_client_secret, code, redirect_uri)
            elif oauth_type == OAUTH_TYPE_NAVER:
                profile_data = self.retrieve_naver_profile(
                    client_id, oauth_setting.naver_client_secret, code, redirect_uri)
            else:
                return None

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
            user.is_active = True
            user.save()
        user.profile.oauth_type = profile_data['oauth_type']
        if not user.profile.email:
            user.profile.email = profile_data['email']
        if not user.profile.name:
            user.profile.name_ko = profile_data['name']
            user.profile.name_en = profile_data['name']
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

    def retrieve_github_profile(self, client_id, client_secret, code, redirect_uri):
        if not client_id or not client_secret:
            raise ValueError(
                'GitHub client information should be registered by admin(OAuthSetting')

        github = OAuth2Session(client_id, redirect_uri=redirect_uri)
        github.fetch_token(GITHUB_ACCESS_TOKEN_URL,
                           client_secret=client_secret, code=code)
        response = github.get(GITHUB_PROFILE_URL)
        response.raise_for_status()
        data = response.json()
        email = data['email']
        if not email:
            email = self.retrieve_github_email(github)
        return {
            'id': data['id'],
            'name': data['login'],
            'avatar_url': data['avatar_url'],
            'email': email,
            'oauth_type': Profile.OAUTH_GITHUB
        }

    def retrieve_github_email(self, github):
        response = github.get(GITHUB_EMAIL_URL)
        response.raise_for_status()
        data = response.json()
        primary_emails = [item['email'] for item in data if item['primary']]
        return primary_emails[0] if primary_emails else None

    def retrieve_google_profile(self, client_id, client_secret, code, redirect_uri):
        if not client_id or not client_secret:
            raise ValueError(
                'Google client information should be registered by admin(OAuthSetting')
        google = OAuth2Session(
            client_id, scope=GOOGLE_SCOPE, redirect_uri=redirect_uri)
        google.fetch_token(GOOGLE_ACCESS_TOKEN_URL,
                           client_secret=client_secret, code=code)
        response = google.get(GOOGLE_PROFILE_URL)
        response.raise_for_status()
        data = response.json()
        return {
            'id': data['id'],
            'name': data['name'],
            'avatar_url': data['picture'],
            'email': data['email'] if 'email' in data else '',
            'oauth_type': Profile.OAUTH_GOOGLE
        }

    def retrieve_facebook_profile(self, client_id, client_secret, code, redirect_uri):
        if not client_id or not client_secret:
            raise ValueError(
                'Facebook client information should be registered by admin(OAuthSetting')
        facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
        facebook.fetch_token(FACEBOOK_ACCESS_TOKEN_URL,
                             client_secret=client_secret, code=code)
        response = facebook.get(FACEBOOK_PROFILE_URL)
        response.raise_for_status()
        data = response.json()
        return {
            'id': data['id'],
            'name': data['name'],
            'avatar_url': data['picture']['data']['url'],
            'email': data['email'] if 'email' in data else '',
            'oauth_type': Profile.OAUTH_FACEBOOK
        }

    def retrieve_naver_profile(self, client_id, client_secret, code, redirect_uri):
        if not client_id or not client_secret:
            raise ValueError(
                'Naver client information should be registered by admin(OAuthSetting')
        naver = OAuth2Session(client_id, redirect_uri=redirect_uri)
        naver.fetch_token(NAVER_ACCESS_TOKEN_URL,
                          client_secret=client_secret, code=code)
        response = naver.get(NAVER_PROFILE_URL)
        response.raise_for_status()
        data = response.json()
        data = data['response']
        return {
            'id': data['id'],
            'name': data['name'],
            'avatar_url': data['profile_image'],
            'email': data['email'],
            'oauth_type': Profile.OAUTH_NAVER
        }
