import os

from core.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from tree_queries.models import TreeNode


def node_cover_path(instance, filename):
    return os.path.join("nodes", "cover", instance.name, filename)


class Node(TimeStampedModel, TreeNode):
    name = models.CharField(_("name"), max_length=30)
    slug = models.SlugField(_("slug"), allow_unicode=True)
    cover = models.ImageField(_("cover"), upload_to=node_cover_path, blank=True)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("node")
        verbose_name_plural = _("nodes")

    def __str__(self):
        return self.name
