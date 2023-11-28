from bx_django_utils.test_utils.html_assertion import HtmlAssertionMixin
from django.contrib.auth.models import User
from django.test import TestCase
from model_bakery import baker

from djfritz import __version__
from djfritz_project.tests.utilities import NoFritzBoxConnection


class AdminAnonymousTests(HtmlAssertionMixin, TestCase):
    """
    Anonymous will be redirected to the login page.
    """

    def test_login(self):
        response = self.client.get('/admin/', secure=False, follow=False)
        self.assertRedirects(
            response, status_code=301, expected_url='https://testserver/admin/', fetch_redirect_response=False
        )
        response = self.client.get('/admin/', secure=True, follow=False)
        self.assertRedirects(
            response, status_code=302, expected_url='/admin/login/?next=/admin/', fetch_redirect_response=False
        )


class AdminLoggedinTests(HtmlAssertionMixin, TestCase):
    """
    Some basics test with the django admin
    """

    @classmethod
    def setUpTestData(cls):
        cls.superuser = baker.make(User, username='superuser', is_staff=True, is_active=True, is_superuser=True)
        cls.staffuser = baker.make(User, username='staff_test_user', is_staff=True, is_active=True, is_superuser=False)

    def test_staff_admin_index(self):
        self.client.force_login(self.staffuser)

        with NoFritzBoxConnection():
            response = self.client.get('/admin/', secure=True, follow=False)
        self.assert_html_parts(
            response,
            parts=(
                f'<title>Site administration | django-fritzconnection v{__version__}</title>',
                '<h1>Site administration</h1>',
                '<strong>staff_test_user</strong>',
                '<a href="/admin/diagnose/test-fritzbox-connection/">Test FritzBox connection</a>',
            ),
        )
        self.assertTemplateUsed(response, template_name='admin/index.html')

    def test_superuser_admin_index(self):
        self.client.force_login(self.superuser)

        with NoFritzBoxConnection():
            response = self.client.get('/admin/', secure=True, follow=False)
        self.assert_html_parts(
            response,
            parts=(
                f'<title>Site administration | django-fritzconnection v{__version__}</title>',
                '<strong>superuser</strong>',
                'Site administration',
                '/admin/auth/group/add/',
                '/admin/auth/user/add/',
            ),
        )
        self.assertTemplateUsed(response, template_name='admin/index.html')
