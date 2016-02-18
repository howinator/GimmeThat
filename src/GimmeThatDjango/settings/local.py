from GimmeThatDjango.settings.base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Need to get dirname of directory above this one since settings is now one module up
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

print(BASE_DIR)
