from .base import *
import_secrets()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.child('db.sqlite3'),
    }
}


STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.child('static')]
STATIC_ROOT = BASE_DIR.child('staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'