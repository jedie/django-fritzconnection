from django.db import models
from django.utils.translation import gettext_lazy as _

from djfritz.models.base import BaseTimetrackingModel


class HostGroupModel(BaseTimetrackingModel):
    name = models.CharField(
        blank=False,
        null=False,
        max_length=63,
        verbose_name=_('HostGroupModel.name.verbose_name'),
        help_text=_('HostGroupModel.name.help_text'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('HostGroupModel.verbose_name')
        verbose_name_plural = _('HostGroupModel.verbose_name_plural')
