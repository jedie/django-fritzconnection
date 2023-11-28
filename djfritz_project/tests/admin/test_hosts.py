import datetime
from unittest import mock

from bx_django_utils.test_utils.datetime import MockDatetimeGenerator
from bx_django_utils.test_utils.html_assertion import (
    HtmlAssertionMixin,
    assert_html_response_snapshot,
)
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from djfritz.models import HostModel
from djfritz_project.tests.utilities import DefaultMocks, NoFritzBoxConnection


class AdminHostsTests1(HtmlAssertionMixin, TestCase):
    def test_anonymous(self):
        response = self.client.get('/admin/djfritz/hostmodel/', secure=True)
        self.assertRedirects(
            response,
            expected_url='/admin/login/?next=/admin/djfritz/hostmodel/',
            fetch_redirect_response=False,
        )


class AdminHostsTests2(HtmlAssertionMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.super_user = baker.make(
            User, username='Mr.Superuser', is_staff=True, is_active=True, is_superuser=True
        )

    def test_empty(self):
        self.client.force_login(user=self.super_user)

        with DefaultMocks(), NoFritzBoxConnection():
            response = self.client.get('/admin/djfritz/hostmodel/', secure=True)

        assert response.status_code == 200
        self.assertTemplateUsed(response, template_name='admin/djfritz/hostmodel/change_list.html')
        self.assert_html_parts(
            response,
            parts=(
                '<title>Select Host to change | django-fritzconnection vMockedVersion</title>',
                '<a href="/admin/djfritz/hostmodel/update_hosts">Update all hosts</a>',
            ),
        )
        assert_html_response_snapshot(response, validate=False)

    @mock.patch.object(timezone, 'now', MockDatetimeGenerator(datetime.timedelta(minutes=1)))
    def test_unique_name_filter(self):
        baker.make(
            HostModel,
            id='00000000-1111-0000-0000-000000000001',
            mac='AB:CD:EF:12:00:01',
            name='unique_name1',
            address_source='DHCP',
            last_status=True,
        )
        baker.make(
            HostModel,
            id='00000000-1111-0000-0000-000000000002',
            mac='AB:CD:EF:12:00:02',
            name='unique_name2',
            address_source='DHCP',
            last_status=True,
        )
        baker.make(
            HostModel,
            id='00000000-1111-0000-0000-000000000003',
            mac='AB:CD:EF:12:00:03',
            name='double_name',
            address_source='DHCP',
            last_status=True,
        )
        baker.make(
            HostModel,
            id='00000000-1111-0000-0000-000000000004',
            mac='AB:CD:EF:12:00:04',
            name='double_name',
            address_source='DHCP',
            last_status=True,
        )

        self.client.force_login(user=self.super_user)

        ###########################################################################################
        # List all:

        with DefaultMocks(), NoFritzBoxConnection():
            response = self.client.get('/admin/djfritz/hostmodel/', secure=True)
        self.assert_html_parts(
            response,
            parts=(
                '<title>Select Host to change | django-fritzconnection vMockedVersion</title>',
                '<td class="field-mac">AB:CD:EF:12:00:01</td>',
                '<td class="field-mac">AB:CD:EF:12:00:02</td>',
                '<td class="field-mac">AB:CD:EF:12:00:03</td>',
                '<td class="field-mac">AB:CD:EF:12:00:04</td>',
            ),
        )
        assert_html_response_snapshot(response, validate=False)

        ###########################################################################################
        # List only unique entries:

        with DefaultMocks(), NoFritzBoxConnection():
            response = self.client.get('/admin/djfritz/hostmodel/?uniqueness=yes', secure=True)
        self.assert_html_parts(
            response,
            parts=(
                '<title>Select Host to change | django-fritzconnection vMockedVersion</title>',
                '<td class="field-mac">AB:CD:EF:12:00:01</td>',
                '<td class="field-mac">AB:CD:EF:12:00:02</td>',
            ),
        )
        self.assert_parts_not_in_html(response, parts=('AB:CD:EF:12:00:03', 'AB:CD:EF:12:00:04'))
        assert_html_response_snapshot(response, validate=False)

        ###########################################################################################
        # List only unique entries:

        with DefaultMocks(), NoFritzBoxConnection():
            response = self.client.get('/admin/djfritz/hostmodel/?uniqueness=no', secure=True)
        self.assert_html_parts(
            response,
            parts=(
                '<title>Select Host to change | django-fritzconnection vMockedVersion</title>',
                '<td class="field-mac">AB:CD:EF:12:00:03</td>',
                '<td class="field-mac">AB:CD:EF:12:00:04</td>',
            ),
        )
        self.assert_parts_not_in_html(response, parts=('AB:CD:EF:12:00:01', 'AB:CD:EF:12:00:02'))
        assert_html_response_snapshot(response, validate=False)
