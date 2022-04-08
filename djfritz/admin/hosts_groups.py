import logging

from django.contrib import admin
from reversion_compare.admin import CompareVersionAdmin

from djfritz.models import HostGroupModel


logger = logging.getLogger(__name__)


@admin.register(HostGroupModel)
class HostGroupModelAdmin(CompareVersionAdmin):
    pass
