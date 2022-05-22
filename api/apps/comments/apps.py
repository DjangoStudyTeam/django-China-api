from django.apps import AppConfig


class CommentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "comments"

    def ready(self):
        from actstream import registry

        from . import signals  # noqa F405

        registry.register(self.get_model("Comment"))
