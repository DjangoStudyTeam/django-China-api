import os

from core.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from tree_queries.fields import TreeNodeForeignKey


def note_cover_path(instance, filename):
    return os.path.join("notes", "cover", instance.name, filename)


class Notes(TimeStampedModel):
    parent = TreeNodeForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("parent"),
        related_name="children",
    )
    name = models.CharField(_("name"), max_length=30)
    slug = models.SlugField(_("slug"), allow_unicode=True)
    cover = models.ImageField(_("cover"), upload_to=note_cover_path, blank=True)
    description = models.CharField(_("description"), max_length=100)

    class Meta(TimeStampedModel.Meta):
        pass
