from unittest.mock import MagicMock, patch

from bx_py_utils.test_utils.context_managers import MassContextManager
from django.template.defaulttags import CsrfTokenNode
from urllib3.exceptions import ProtocolError

from djfritz import context_processors


class DenyCallError(SystemExit):
    pass


class DenyCall:
    def __init__(self, func_name):
        self.func_name = func_name

    def __call__(self, *args, **kwargs):
        raise DenyCallError(f'Deny {self.func_name} call with: {args=} {kwargs=}')


class DenyAnyRealRequestContextManager(MassContextManager):
    mocks = (
        patch('socket.create_connection', DenyCall('socket create_connection()')),
        patch('urllib3.util.connection.create_connection', DenyCall('urllib3 create_connection()')),
    )


def deny_any_real_request():
    cm = DenyAnyRealRequestContextManager()
    cm.__enter__()


class DefaultMocks(MassContextManager):
    def __init__(self):
        version_mock = MagicMock()
        version_mock.__str__.return_value = 'MockedVersion'
        self.mocks = [
            patch.object(CsrfTokenNode, 'render', return_value='MockedCsrfTokenNode'),
            patch.object(context_processors, '__version__', new=version_mock),
        ]


class NoFritzBoxConnection(MassContextManager):
    def __init__(self):
        self.mocks = [
            patch(
                'urllib3.util.connection.create_connection',
                side_effect=ProtocolError('<Mocked urllib3 in tests>'),
            ),
        ]
