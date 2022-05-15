# flake8: noqa: E405, F403

import requests_mock

from djfritz_project.settings.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'No individual secret... But this settings should only be used in tests ;)'

# Run the tests as on production: Without DBEUG:
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ('127.0.0.1', '0.0.0.0', 'localhost')


###################################################################################################
# Deny any not mocked requests


def _unmocked_requests_error_message(request, response):
    raise RuntimeError(
        f'Unmocked request to {request.url} in tests, wrap with requests_mock.mock()!'
    )


fallback_mocker = requests_mock.Mocker()
fallback_mocker.get(requests_mock.ANY, content=_unmocked_requests_error_message)
fallback_mocker.__enter__()


###################################################################################################


LOGGING['formatters']['colored']['format'] = (
    '%(log_color)s%(name)s %(levelname)8s %(cut_path)s:%(lineno)-3s %(message)s'
)
