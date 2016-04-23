from GimmeThatDjango.settings.base import *

DEBUG = True
#ALLOWED_HOSTS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Need to get dirname of directory above this one since settings is now
# one module up
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    #    '/var/www/static/',
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_CDN")

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_CDN")

DB_PASSWORD = get_env_variable("DB_PASSWORD")
DB_USER = get_env_variable("DB_USER")

DATABASES = {
    "default": {
        "NAME": "gimmethatdb",
        "HOST": "localhost",
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "PORT": ""
    }
}

