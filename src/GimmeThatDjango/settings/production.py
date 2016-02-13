from GimmeThatDjango.settings.base import *

DEBUG = False

DB_PASSWORD = base.get_env_variable(DB_PASSWORD)
DB_USER = base.get_env_variable(DB_USER)

DATABASES = {
    "default": {
        "NAME": "gimmethatdb",
        "HOST": "localhost",
        "USER": "gimmethatdbuser",
        "PASSWORD": DB_PASSWORD,
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "PORT": ""
    }
}
