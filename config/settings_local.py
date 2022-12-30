from .settings import *

from botocore.config import Config

AWS_CONFIG = Config(
    region_name = 'ap-northeast-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 3,
        'mode': 'standard'
    }
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}
DEBUG = True

SITE_URL = 'http://localhost:3000'

KAKAO_REST_API_KEY = '784d5eb4b69acdedc342cab868befa1a'
