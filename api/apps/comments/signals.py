from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification

from .models import Comment


@receiver(post_save, sender=Comment, dispatch_uid="my_unique_identifier")
def my_handler(sender, instance, **kwargs):
    Notification.objects.create(content=f"{instance.user} give you a comment", recipient=instance.user)
