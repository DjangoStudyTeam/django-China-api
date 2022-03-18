from django.db.models.signals import Signal
from django.dispatch import receiver
from notifications.models import Notification

comment_posted = Signal(providing_args=["instance", "content_type"])


@receiver(comment_posted)
def my_handler(sender, instance, content_type, **kwargs):
    Notification.objects.create(
        content=f"{instance.post.user}给你发送了1条评论,内容是{instance.content}",
        actor=instance.user,
        recipient=instance.post.user,
        action_object_content_type=content_type,
        action_object_object_id=instance.id,
    )
