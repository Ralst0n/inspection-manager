from .base import *
from decouple import config

DEBUG = config('DJANGO_DEBUG', True)

SECRET_KEY = config('DJANGO_SECRET_KEY')

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'Password': config('DATABASE_PASS'),
        'HOST': 'localhost',
        'PORT': '',
    }
}