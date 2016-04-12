from GimmeThatDjango.settings.base import *

DEBUG = False

# Ensure HTTPS security

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

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

ALLOWED_HOSTS = [".gimmeth.at", "127.0.0.1", "localhost"]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_CDN")

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_CDN")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False
SERVER_EMAIL = 'howie@gimmeth.at'
