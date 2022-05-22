from actstream.signals import action as action_signal
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from notifications.models import Notification
from tree_comments import get_comment_model
from tree_comments.signals import comment_posted

Comment = get_comment_model()


@receiver(comment_posted)
def comment_posted_handler(sender, comment, request, **kwargs):
    verb = "reply" if comment.parent_id else "comment"
    action_signal.send(request.user, verb=verb, target=comment, action_object=comment.post)

    Notification.objects.create(
        content="",
        actor=request.user,
        recipient=comment.post.user,
        action_object_content_type=ContentType.objects.get_for_model(Comment),
        action_object_object_id=comment.id,
    )
