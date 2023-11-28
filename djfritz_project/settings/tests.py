# flake8: noqa: E405
"""
    Settings used to run tests
"""
from djfritz_project.settings.prod import *  # noqa


# _____________________________________________________________________________
# Manage Django Project

INSTALLED_APPS.append('manage_django_project')

# _____________________________________________________________________________


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'This is not a individual secret string, because this is only used for tests ;)'

DEBUG = True

# Speedup tests by change the Password hasher:
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)

# _____________________________________________________________________________

# Skip download map via geotiler in djfritz.gpx_tools.gpxpy2map.generate_map
MAP_DOWNLOAD = False


# All tests should use django-override-storage!
# Set root to not existing path, so that wrong tests will fail:
STATIC_ROOT = '/not/exists/static/'
MEDIA_ROOT = '/not/exists/media/'
