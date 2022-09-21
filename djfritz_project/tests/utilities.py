from unittest import mock
from unittest.mock import MagicMock, patch

from django.template.defaulttags import CsrfTokenNode
from fritzconnection.core.exceptions import FritzConnectionException

from djfritz import context_processors, fritz_connection


class MocksBase:
    mocks = None  # Should be set in __init__ !

    def __enter__(self):
        assert self.mocks
        for mock in self.mocks:
            mock.__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for mock in self.mocks:
            mock.__exit__(exc_type, exc_val, exc_tb)


class DefaultMocks(MocksBase):
    def __init__(self):
        version_mock = MagicMock()
        version_mock.__str__.return_value = 'MockedVersion'
        self.mocks = [
            patch.object(CsrfTokenNode, 'render', return_value='MockedCsrfTokenNode'),
            patch.object(context_processors, '__version__', new=version_mock),
        ]


class NoFritzBoxMocks(MocksBase):
    def __init__(self):
        self.mocks = [
            mock.patch.object(
                fritz_connection,
                'FritzConnection',
                side_effect=FritzConnectionException('test mock'),
            )
        ]
