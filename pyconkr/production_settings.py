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

aws_env_keys = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_STORAGE_BUCKET_NAME']

for key in aws_env_keys:
    if not os.getenv(key):
        print(f'You should set {key} into ~/.profile')
        exit(1)

AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'ap-northeast-2'
AWS_S3_SIGNATURE_VERSION = 's3v4'

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

# Sentry
sentry_sdk.init(
    dsn="https://6fe01f813872470f98867604b39cd9e8@sentry.io/1473357",
    environment='production',
    integrations=[DjangoIntegration()]
)
