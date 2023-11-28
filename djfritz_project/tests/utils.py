import shutil
from pathlib import Path
from unittest import TestCase

# https://github.com/jedie/django-tools
from django_tools.unittest_utils.django_command import DjangoCommandMixin


class ForRunnersCommandTestCase(DjangoCommandMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        # installed via setup.py entry points !
        cls.django_fritzconnection_bin = shutil.which("django_fritzconnection")
        cls.manage_bin = shutil.which("manage")

    def _call_django_fritzconnection(self, cmd, **kwargs):
        django_fritzconnection_path = Path(self.django_fritzconnection_bin)
        return self.call_manage_py(
            cmd=cmd,
            manage_dir=django_fritzconnection_path.parent,
            manage_py=django_fritzconnection_path.name,
            **kwargs,
        )

    def _call_manage(self, cmd, **kwargs):
        manage_path = Path(self.manage_bin)
        return self.call_manage_py(
            cmd=cmd,
            manage_dir=manage_path.parent,
            manage_py=manage_path.name,
            **kwargs,
        )
