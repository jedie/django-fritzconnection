"""
    Import all "admin_views" to register them with @register_admin_view decorator
"""
from importlib import import_module
from pathlib import Path


def _register_all_admin_extra_views():
    for item in Path(__file__).parent.glob('*.py'):
        file_name = item.stem
        if file_name.startswith('_'):
            continue

        import_module(f'{__name__}.{file_name}')


_register_all_admin_extra_views()
