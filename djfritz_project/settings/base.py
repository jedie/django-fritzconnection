"""
    Base Django settings
"""

import logging
from pathlib import Path as __Path

from django.utils.translation import gettext_lazy as _


###############################################################################

# Build paths relative to the project root:
PROJECT_PATH = __Path(__file__).parent.parent.parent
print(f'PROJECT_PATH:{PROJECT_PATH}')

if __Path('/.dockerenv').is_file():
    # We are inside a docker container
    BASE_PATH = __Path('/django_volumes')
    assert BASE_PATH.is_dir()
else:
    # Build paths relative to the current working directory:
    BASE_PATH = __Path().cwd().resolve()

print(f'BASE_PATH:{BASE_PATH}')

# Paths with Django dev. server:
# BASE_PATH...: .../django-for-runners
# PROJECT_PATH: .../django-for-runners/src
#
# Paths in Docker container:
# BASE_PATH...: /for_runners_volumes
# PROJECT_PATH: /usr/local/lib/python3.9/site-packages

###############################################################################


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

# Serve static/media files by Django?
# In production Caddy should serve this!
SERVE_FILES = False


# SECURITY WARNING: keep the secret key used in production secret!
__SECRET_FILE = __Path(BASE_PATH, 'secret.txt').resolve()
if not __SECRET_FILE.is_file():
    print(f'Generate {__SECRET_FILE}')
    from secrets import token_urlsafe as __token_urlsafe

    __SECRET_FILE.open('w').write(__token_urlsafe(128))

SECRET_KEY = __SECRET_FILE.open('r').read().strip()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'bx_django_utils',  # https://github.com/boxine/bx_django_utils

    'djfritz.apps.DjFritzConfig',
]

ROOT_URLCONF = 'djfritz_project.urls'
WSGI_APPLICATION = 'djfritz_project.wsgi.application'
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(__Path(PROJECT_PATH, 'djfritz_project', 'templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'djfritz.context_processors.djfritz_version_string',
            ],
        },
    },
]

# _____________________________________________________________________________

# Mark CSRF cookie as "secure" -> browsers sent cookie only with an HTTPS connection:
CSRF_COOKIE_SECURE = True

# Mark session cookie as "secure" -> browsers sent cookie only with an HTTPS connection:
SESSION_COOKIE_SECURE = True

# HTTP header/value combination that signifies a request is secure
# Your nginx.conf must set "X-Forwarded-Protocol" proxy header!
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

# SecurityMiddleware should redirects all non-HTTPS requests to HTTPS:
SECURE_SSL_REDIRECT = True

# SecurityMiddleware should preload directive to the HTTP Strict Transport Security header:
SECURE_HSTS_PRELOAD = True

# Instruct modern browsers to refuse to connect to your domain name via an insecure connection:
SECURE_HSTS_SECONDS = 3600

# SecurityMiddleware should add the "includeSubDomains" directive to the Strict-Transport-Security
# header: All subdomains of your domain should be served exclusively via SSL!
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# _____________________________________________________________________________
# Internationalization

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]
USE_I18N = True
USE_L10N = True
TIME_ZONE = 'Europe/Paris'
USE_TZ = True

# _____________________________________________________________________________
# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = str(__Path(BASE_PATH, 'static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = str(__Path(BASE_PATH, 'media'))


# _____________________________________________________________________________
# cut 'pathname' in log output

old_factory = logging.getLogRecordFactory()


def cut_path(pathname, max_length):
    if len(pathname) <= max_length:
        return pathname
    return f'...{pathname[-(max_length - 3):]}'


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.cut_path = cut_path(record.pathname, 30)
    return record


logging.setLogRecordFactory(record_factory)

# -----------------------------------------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'colored': {  # https://github.com/borntyping/python-colorlog
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s %(levelname)8s %(cut_path)s:%(lineno)-3s %(message)s',
        }
    },
    'handlers': {'console': {'class': 'colorlog.StreamHandler', 'formatter': 'colored'}},
    'loggers': {
        '': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
        'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'axes': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
        'django_tools': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'djfritz': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
    },
}
