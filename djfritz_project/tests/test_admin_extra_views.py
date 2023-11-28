from bx_django_utils.admin_extra_views.utils import iter_admin_extra_views_urls
from bx_py_utils.test_utils.snapshot import assert_snapshot
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from djfritz.fritz_connection import get_fritz_connection
from djfritz_project.tests.utilities import NoFritzBoxConnection


@override_settings(SECURE_SSL_REDIRECT=False)
class AdminExtraViewsTestCase(TestCase):
    """
    Integrations tests for Admin Extra Views.
    """

    def test_anonymous_access(self):
        checked_urls = 0
        for url in iter_admin_extra_views_urls():
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            checked_urls += 1
        self.assertGreaterEqual(checked_urls, 1)

    def test_superuser_access(self):
        assert reverse('admin:index') == '/admin/'

        superuser = User.objects.create_superuser(username='foobar')
        self.client.force_login(superuser)

        with NoFritzBoxConnection():
            self.assertIs(get_fritz_connection(), None)  # Mock works?

            all_urls = []
            for url in iter_admin_extra_views_urls():
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                all_urls.append(url)
            self.assertGreaterEqual(len(all_urls), 1)
            assert_snapshot(got=all_urls)
