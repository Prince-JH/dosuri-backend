"""
Django config for dosuri project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of config and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEV_ENV = os.environ.get('DEV_ENV')
secret_file = os.path.join(f'{BASE_DIR}/config', 'secret.json')

DOSURI_IMAGE_PUBLIC_KEY_ID = os.environ.get('DOSURI_IMAGE_PUBLIC_KEY_ID')
DOSURI_IMAGE_PRIVATE_KEY_PATH = os.environ.get('DOSURI_IMAGE_PRIVATE_KEY_PATH')

HOST_DOMAIN = os.environ.get('HOST_DOMAIN')
# SECURITY WARNING: keep the secret key used in production secret!
with open(secret_file, encoding='utf-8') as fin:
    secrets = json.loads(fin.read())
    SECRET_KEY = secrets.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
APPEND_SLASH = False

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['dosuri-env.eba-igc5wtjb.ap-northeast-2.elasticbeanstalk.com', '127.0.0.1']

CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'dosuri.apps.DosuriConfig',
    'drf_spectacular',
    'corsheaders',
    'django_celery_beat',
]
# if DEBUG:
#     INSTALLED_APPS.append('drf_spectacular')

AUTH_USER_MODEL = 'dosuri.User'
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEV_ENV == 'prod':
    MIDDLEWARE.append('dosuri.common.es.es_middleware')

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'dosuri.common.pagings.PageSizeResultsSetPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'SIGNING_KEY': SECRET_KEY,
    'ALGORITHM': 'HS256'
}

ROOT_URLCONF = 'dosuri.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


DEBUG = True
if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

SITE_URL = os.environ.get('SITE_URL')
SERVER_URL = os.environ.get('SERVER_URL', '')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'dosuri')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
KAKAO_REST_API_KEY = os.environ.get('KAKAO_REST_API_KEY')
KAKAO_REDIRECT_URI = os.environ.get('KAKAO_REDIRECT_URI')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
CONTENT_STORAGE = {
    "class": "storages.backends.s3boto3.S3Boto3Storage",
    "kwargs": {
        "bucket_name": "dosuri-content"
    }
}
ES_ENDPOINT = os.environ.get('ES_ENDPOINT')
ES_USERNAME = os.environ.get('ES_USERNAME')
ES_PASSWORD = os.environ.get('ES_PASSWORD')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_SNS_TOPIC_ARN = os.environ.get('AWS_SNS_TOPIC_ARN')
NAVER_CLOUD_ACCESS_KEY_ID = os.environ.get('NAVER_CLOUD_ACCESS_KEY_ID')
NAVER_CLOUD_SECRET_KEY = os.environ.get('NAVER_CLOUD_SECRET_KEY')
NAVER_CLOUD_FROM_NUMBER = os.environ.get('NAVER_CLOUD_FROM_NUMBER')
INSURANCE_PHONE_NUMBERS = os.environ.get('INSURANCE_PHONE_NUMBERS', [])
