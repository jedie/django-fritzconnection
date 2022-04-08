import uuid

import tagulous.models
from bx_django_utils.models.timetracking import TimetrackingBaseModel
from django.contrib.admin.utils import quote
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BaseTimetrackingModel(TimetrackingBaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('BaseModel.id.verbose_name'),
        help_text=_('BaseModel.id.help_text'),
    )

    def get_change_url(self):
        opts = self._meta
        url = reverse(
            f'admin:{opts.app_label}_{opts.model_name}_change',
            args=(quote(self.pk),),
        )
        return url

    class Meta:
        abstract = True


class BaseTimetrackingTaggedModel(BaseTimetrackingModel):
    tags = tagulous.models.TagField(
        blank=True,
        case_sensitive=False,
        force_lowercase=False,
        space_delimiter=False,
        max_count=10,
        verbose_name=_('BaseModel.tags.verbose_name'),
        help_text=_('BaseModel.tags.help_text'),
    )

    class Meta:
        abstract = True
