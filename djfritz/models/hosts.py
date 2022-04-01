from django.contrib.admin.utils import quote
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from djfritz.fritz_connection import FritzHostFilter
from djfritz.models.base import BaseTimetrackingTaggedModel


class HostModel(BaseTimetrackingTaggedModel):
    mac = models.CharField(
        # Stored in "RAW" format from FritzBox
        # uppercase with colons, e.g.: "AB:CD:EF:12:34:56"
        unique=True,
        db_index=True,
        blank=False,
        null=False,
        max_length=17,
        verbose_name=_('HostModel.mac.verbose_name'),
        help_text=_('HostModel.mac.help_text'),
    )
    ip_v4 = models.GenericIPAddressField(
        protocol='IPv4',
        blank=True,
        null=True,
        verbose_name=_('HostModel.ip_v4.verbose_name'),
        help_text=_('HostModel.ip_v4.help_text'),
    )
    ip_v6 = models.GenericIPAddressField(
        protocol='IPv6',
        blank=True,
        null=True,
        verbose_name=_('HostModel.ip_v6.verbose_name'),
        help_text=_('HostModel.ip_v6.help_text'),
    )
    name = models.CharField(
        blank=False,
        null=False,
        max_length=63,  # Max length of FritzBox host names ;)
        verbose_name=_('HostModel.name.verbose_name'),
        help_text=_('HostModel.name.help_text'),
    )
    last_status = models.BooleanField(
        # Is this host was active or not?
        null=False,
        verbose_name=_('HostModel.last_status.verbose_name'),
        help_text=_('HostModel.last_status.help_text'),
    )
    interface_type = models.CharField(
        # e.g.: "Ethernet",  "802.11", "HomePlug" or None
        blank=True,
        null=True,
        max_length=8,
        verbose_name=_('HostModel.interface_type.verbose_name'),
        help_text=_('HostModel.interface_type.help_text'),
    )
    address_source = models.CharField(
        # e.g.: "Static" or "DHCP"
        blank=False,
        null=False,
        max_length=6,
        verbose_name=_('HostModel.address_source.verbose_name'),
        help_text=_('HostModel.address_source.help_text'),
    )
    lease_time_remaining = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name=_('HostModel.lease_time_remaining.verbose_name'),
        help_text=_('HostModel.lease_time_remaining.help_text'),
    )

    WAN_ACCESS_STATE_CHOICES = [
        (FritzHostFilter.WAN_ACCESS_STATE_GRANTED, _('granted')),
        (FritzHostFilter.WAN_ACCESS_STATE_DENIED, _('denied')),
        (FritzHostFilter.WAN_ACCESS_STATE_ERROR, _('error')),
        (FritzHostFilter.WAN_ACCESS_STATE_UNKNOWN, _('unknown')),
    ]
    WAN_ACCESS_STATE_CHOICES_DICT = dict(WAN_ACCESS_STATE_CHOICES)

    wan_access = models.CharField(
        max_length=max(len(key) for key in WAN_ACCESS_STATE_CHOICES_DICT.keys()),
        choices=WAN_ACCESS_STATE_CHOICES,
        default=FritzHostFilter.WAN_ACCESS_STATE_UNKNOWN,
        editable=False,
        verbose_name=_('HostModel.wan_access.verbose_name'),
        help_text=_('HostModel.wan_access.help_text'),
    )

    def __str__(self):
        return f'Host "{self.name}" ({self.mac})'

    def get_change_url(self):
        opts = self._meta
        url = reverse(
            f'admin:{opts.app_label}_{opts.model_name}_change',
            args=(quote(self.pk),),
        )
        return url

    class Meta:
        verbose_name = _('HostModel.verbose_name')
        verbose_name_plural = _('HostModel.verbose_name_plural')
