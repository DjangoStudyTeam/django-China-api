from core.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Title(TimeStampedModel):
    word = models.CharField(_("word"), max_length=50)

    class Meta:
        verbose_name = _("title")
        verbose_name_plural = _("titles")

    def __str__(self):
        return self.word
