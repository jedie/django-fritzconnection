import uuid

import tagulous.models
from bx_django_utils.models.timetracking import TimetrackingBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseTimetrackingTaggedModel(TimetrackingBaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('BaseModel.id.verbose_name'),
        help_text=_('BaseModel.id.help_text'),
    )
    tags = tagulous.models.TagField(
        blank=True,
        case_sensitive=False,
        force_lowercase=False,
        space_delimiter=False,
        max_count=10,
        verbose_name=_('BaseModel.tags.verbose_name'),
        help_text=_('BaseModel.tags.help_text'),
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
