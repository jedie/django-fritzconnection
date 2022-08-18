import os
import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.core import checks
from django.core.cache import cache
from django.test import TestCase

import djfritz


PACKAGE_ROOT = Path(djfritz.__file__).parent.parent


def assert_file_contains_string(file_path, string):
    with file_path.open('r') as f:
        for line in f:
            if string in line:
                return
    raise AssertionError(f'File {file_path} does not contain {string!r} !')


def test_version(package_root=None, version=None):
    if package_root is None:
        package_root = PACKAGE_ROOT

    if version is None:
        version = djfritz.__version__

    if 'dev' not in version and 'rc' not in version:
        version_string = f'v{version}'

        assert_file_contains_string(
            file_path=Path(package_root, 'README.md'), string=version_string
        )

    assert_file_contains_string(
        file_path=Path(package_root, 'pyproject.toml'), string=f'version = "{version}"'
    )


def test_poetry_check(package_root=None):
    if package_root is None:
        package_root = PACKAGE_ROOT

    poerty_bin = shutil.which('poetry')

    output = subprocess.check_output(
        [poerty_bin, 'check'],
        text=True,
        env=os.environ,
        stderr=subprocess.STDOUT,
        cwd=str(package_root),
    )
    print(output)
    assert output == 'All set!\n'


class ProjectSettingsTestCase(TestCase):
    def test_base_path(self):
        base_path = settings.BASE_PATH
        assert base_path.is_dir()
        assert Path(base_path, 'djfritz').is_dir()
        assert Path(base_path, 'djfritz_project').is_dir()

    def test_template_dirs(self):
        assert len(settings.TEMPLATES) == 1
        dirs = settings.TEMPLATES[0].get('DIRS')
        assert len(dirs) == 1
        template_path = Path(dirs[0]).resolve()
        assert template_path.is_dir()

    def test_manage_check(self):
        all_issues = checks.run_checks(
            app_configs=None,
            tags=None,
            include_deployment_checks=True,
            databases=None,
        )
        if all_issues:
            print('=' * 100)
            for issue in all_issues:
                print(issue)
            print('=' * 100)
            raise AssertionError('There are check issues!')

    def test_cache(self):
        # django cache should work in tests, because some tests "depends" on it
        cache_key = 'a-cache-key'
        assert cache.get(cache_key) is None
        cache.set(cache_key, 'the cache content', timeout=1)
        assert cache.get(cache_key) == 'the cache content'
        cache.delete(cache_key)
        assert cache.get(cache_key) is None

    def test_settings(self):
        assert settings.SETTINGS_MODULE == 'djfritz_project.settings.tests'
        middlewares = [entry.rsplit('.', 1)[-1] for entry in settings.MIDDLEWARE]
        assert 'AlwaysLoggedInAsSuperUserMiddleware' not in middlewares
        assert 'DebugToolbarMiddleware' not in middlewares
