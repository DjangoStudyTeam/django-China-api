from core.models import TimeStampedModel
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.fields import MonitorField
from nodes.models import Node


class Post(TimeStampedModel):
    title = models.CharField(_("title"), max_length=150)
    body = models.TextField(_("body"), blank=True)
    views = models.IntegerField(_("views"), default=0)
    pinned = models.BooleanField(_("pinned"), default=False)
    highlighted = models.BooleanField(_("highlighted"), default=False)
    deleted = models.BooleanField(_("deleted"), default=False)
    edited_at = MonitorField(_("edited at"), monitor=body)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="user",
        related_name="posts",
    )
    node = models.ForeignKey(
        Node, on_delete=models.CASCADE, verbose_name="node", related_name="posts"
    )

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return self.title
