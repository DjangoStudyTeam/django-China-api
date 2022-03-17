from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from notifications_plus.models import AbstractNotification


class Notification(AbstractNotification):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("recipient"),
        related_name="notification",
        on_delete=models.CASCADE,
    )
    action_object_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="notifications",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "notification"
        verbose_name_plural = "notifications"
