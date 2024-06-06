from .base import *
import os
from decouple import config
import dj_database_url
import django_heroku

DEBUG = False

ALLOWED_HOSTS = ['quiensuma.com', 'quiensuma-app.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WhiteNoise to serve static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Activate Django-Heroku.
django_heroku.settings(locals())
