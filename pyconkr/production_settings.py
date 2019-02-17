# pylint: disable=unused-wildcard-import,wildcard-import
from pyconkr.settings import *

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pyconkr',
        'USER': 'pyconkr',
        'HOST': 'db',
        'PORT': 5432,
    }
}
