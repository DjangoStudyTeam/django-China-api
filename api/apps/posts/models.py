from core.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.fields import MonitorField
from nodes.models import Node

User = get_user_model()


class Post(TimeStampedModel):
    title = models.CharField(_("title"), max_length=150)
    body = models.TextField(_("body"), blank=True)
    views = models.IntegerField(_("views"), default=0)
    pinned = models.IntegerField(_("pinned"), default=0)
    highlighted = models.IntegerField(_("highlighted"), default=0)
    deleted = models.IntegerField(_("deleted"), default=0)
    edited_at = MonitorField(_("edited_at"), monitor=body)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
