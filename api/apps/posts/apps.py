from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "posts"
    verbose_name = _("Posts")

    def ready(self):
        from actstream import registry
        from actstream.actions import action_handler as actstream_action_handler
        from actstream.signals import action as action_signal
        from core.receivers import action_handler

        action_signal.disconnect(actstream_action_handler, dispatch_uid="actstream.models")
        action_signal.connect(action_handler, dispatch_uid="actstream.models")

        registry.register(self.get_model("Post"))
