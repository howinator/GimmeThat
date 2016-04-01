from GimmeThatDjango.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Need to get dirname of directory above this one since settings is now
# one module up
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    #    '/var/www/static/',
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_CDN")

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_CDN")
