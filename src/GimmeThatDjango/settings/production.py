from GimmeThatDjango.settings.base import *

DEBUG = False

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

ALLOWED_HOSTS = [".gimmeth.at"]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_CDN")

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_CDN")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    #    '/var/www/static/',
]
