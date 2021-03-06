from pathlib import Path

from poetry_publish.publish import poetry_publish
from poetry_publish.utils.subprocess_utils import verbose_check_call

# https://github.com/jedie/django-fritzconnection
import djfritz


PACKAGE_ROOT = Path(djfritz.__file__).parent.parent.parent


def publish():
    """
    Publish to PyPi
    Call this via:
        $ poetry run publish
    """
    verbose_check_call('make', 'pytest')  # don't publish if tests fail
    verbose_check_call('make', 'fix-code-style')  # don't publish if code style wrong

    poetry_publish(
        package_root=PACKAGE_ROOT,
        version=djfritz.__version__,
        creole_readme=True,  # don't publish if README.rst is not up-to-date
    )
