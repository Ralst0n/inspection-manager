from .base import *
from decouple import config

import django
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
ALLOWED_HOSTS = ['prudentoffice.herokuapp.com',]
django.setup()


AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'prudent-office-assets'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'

DEFAULT_FILE_STORAGE = 'config.settings.storage_backends.MediaStorage' 

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media"