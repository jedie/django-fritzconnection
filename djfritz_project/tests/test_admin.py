import logging

from bx_django_utils.test_utils.html_assertion import (
    HtmlAssertionMixin,
    assert_html_response_snapshot,
)
from django.contrib.auth.models import User
from django.test import TestCase

from djfritz.fritz_connection import get_fritz_connection
from djfritz_project.tests.utilities import DefaultMocks, NoFritzBoxMocks


class AdminTests(HtmlAssertionMixin, TestCase):
    def test_login_en(self):
        response = self.client.get('/admin/', secure=True, HTTP_ACCEPT_LANGUAGE='en')
        self.assertRedirects(
            response, expected_url='/admin/login/?next=/admin/', fetch_redirect_response=False
        )

    def test_login_de(self):
        response = self.client.get('/admin/', secure=True, HTTP_ACCEPT_LANGUAGE='de')
        self.assertRedirects(
            response, expected_url='/admin/login/?next=/admin/', fetch_redirect_response=False
        )

    def test_index_redirect(self):
        response = self.client.get('/', secure=True)
        self.assertRedirects(
            response,
            expected_url='/admin/login/?next=%2Fadmin%2Fmanagement%2Fmanage-host-wan-access-via-host-groups%2F',
            fetch_redirect_response=False,
        )

        with self.assertLogs('django.request', level=logging.WARNING):
            response = self.client.get(
                '/admin/management/manage-host-wan-access-via-host-groups/', secure=True
            )
        self.assertEqual(response.status_code, 403)

    def test_admin_index_page(self):
        self.client.force_login(User.objects.create_superuser(username='foobar'))
        with NoFritzBoxMocks(), DefaultMocks():
            assert get_fritz_connection() is None  # Mock works?

            response = self.client.get('/admin/', secure=True)
            self.assertEqual(response.status_code, 200)
            self.assert_html_parts(
                response,
                parts=(
                    '<title>Site administration | django-fritzconnection vMockedVersion</title>',
                    '<a href="/admin/diagnose/list-all-fritzbox-services/">List all FritzBox services</a>',
                ),
            )
            assert_html_response_snapshot(response, validate=False)
