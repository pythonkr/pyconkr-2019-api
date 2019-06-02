# pylint: disable=unused-wildcard-import,wildcard-import
from pyconkr.settings import *

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'pythonkoreadb.c3lemconopmq.ap-northeast-2.rds.amazonaws.com',
        'NAME': 'pycondev',
        'USER': 'pycondev',
        'PASSWORD': 'pycondevAAZZZ**',
        'PORT': 25432,
    }
}

aws_env_keys = ['DEV_AWS_ACCESS_KEY_ID', 'DEV_AWS_SECRET_ACCESS_KEY', 'DEV_AWS_STORAGE_BUCKET_NAME']

for key in aws_env_keys:
    if not os.getenv(key):
        print(f'You should set {key} into ~/.profile')
        exit(1)

AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('DEV_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('DEV_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('DEV_AWS_STORAGE_BUCKET_NAME')
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
