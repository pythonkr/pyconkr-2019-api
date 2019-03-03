# pylint: disable=unused-wildcard-import,wildcard-import
from pyconkr.settings import *

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

MEDIA_ROOT = '/media'
STATIC_ROOT = '/static'
MEDIA_URL = 'http://www.pycon.kr/media/'
