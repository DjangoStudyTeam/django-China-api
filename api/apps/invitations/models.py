from core.models import TimeStampedModel
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


class Invitation(TimeStampedModel):
    CODE_LENGTH = 8
    CODE_ALLOWED_CHARS = "0123456789"

    code = models.CharField(_("code"), max_length=CODE_LENGTH, unique=True)
    expire_at = models.DateTimeField(_("expire at"), blank=True, null=True)
    valid = models.BooleanField(_("valid"), default=True, editable=False)
    invalidated_at = models.DateTimeField(_("invalidated at"), blank=True, null=True)
    special = models.BooleanField(_("special"), default=False)
    titles = models.ManyToManyField("titles.Title", blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name=_("creator"),
        null=True,
        related_name="invitations",
    )
    invitee = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name=_("invitee"),
        null=True,
        related_name="invitation",
    )

    class Meta:
        verbose_name = _("invitation")
        verbose_name_plural = _("invitations")

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.gen_code()
        super().save(*args, **kwargs)

    @admin.display(boolean=True)
    def expired(self):
        if self.expire_at is None:
            return False
        return timezone.now() > self.expire_at

    @classmethod
    def gen_code(cls):
        while True:
            code = get_random_string(cls.CODE_LENGTH, cls.CODE_ALLOWED_CHARS)
            if not Invitation.objects.filter(code=code).exists():
                return code
