from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NodesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nodes"
    verbose_name = _("Nodes")
