from .base import *
from decouple import config

import dj_database_url
import django_heroku

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

DEBUG = config('DJANGO_DEBUG', default=False)

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

SECRET_KEY = config('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['https://prudentoffice.herokuapp.com/',]

# Activate Django-Heroku.
django_heroku.settings(locals())