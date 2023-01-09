from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'dosuri-test',
        'USER': 'postgres',
        'PASSWORD': 'dosuri',
    }
}
