# pylint: disable=unused-wildcard-import,wildcard-import
from pyconkr.settings import *


DEBUG = False
ALLOWED_HOSTS = ['*']

db_env_keys = ['PYCONKR_POSTGRES_HOST', 'PYCONKR_POSTGRES_NAME', 'PYCONKR_POSTGRES_PORT',
               'PYCONKR_POSTGRES_USER', 'PYCONKR_POSTGRES_PASSWORD']

for key in db_env_keys:
    if not os.getenv(key):
        print(f'You should set {key} into ~/.profile')
        exit(1)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PYCONKR_POSTGRES_NAME'),
        'HOST': os.getenv('PYCONKR_POSTGRES_HOST'),
        'PORT': os.getenv('PYCONKR_POSTGRES_PORT'),
        'USER': os.getenv('PYCONKR_POSTGRES_USER'),
        'PASSWORD': os.getenv('PYCONKR_POSTGRES_PASSWORD'),
    }
}

# MEDIA_ROOT = '/media'
# MEDIA_URL = 'https://www.pycon.kr/api/media/'
# STATIC_URL = '/api/static/'
# STATIC_ROOT = '/static'

aws_env_keys = ['PROD_AWS_ACCESS_KEY_ID', 'PROD_AWS_SECRET_ACCESS_KEY', 'PROD_AWS_STORAGE_BUCKET_NAME']

for key in aws_env_keys:
    if not os.getenv(key):
        print(f'You should set {key} into ~/.profile')
        exit(1)

AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('PROD_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('PROD_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('PROD_AWS_STORAGE_BUCKET_NAME')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/log/error.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['file', 'console', ],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
