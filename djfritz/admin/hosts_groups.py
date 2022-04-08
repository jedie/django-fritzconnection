import logging
from uuid import UUID

from bx_django_utils.models.manipulate import CreateOrUpdateResult
from django.contrib import admin, messages
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from fritzconnection.core.exceptions import FritzConnectionException
from reversion_compare.admin import CompareVersionAdmin

from djfritz.models import HostGroupModel, HostModel
from djfritz.services.hosts import set_wan_access_state, update_host, update_hosts


logger = logging.getLogger(__name__)


# class HostModelInline(admin.TabularInline):
#     model = HostModel


@admin.register(HostGroupModel)
class HostGroupModelAdmin(CompareVersionAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
