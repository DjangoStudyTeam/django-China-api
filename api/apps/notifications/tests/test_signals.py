from django.urls import reverse
from notifications.models import Notification
from posts.tests.factories import PostFactory
from rest_framework.test import APIClient


def test_comment_posted_handler(admin_user):
    post = PostFactory()

    api_client = APIClient()
    api_client.force_login(admin_user)
    url = reverse("api:comment-list")
    api_client.post(url, data={"post": post.id, "content": "test"})

    assert Notification.objects.count() == 1

    notification = Notification.objects.get()
    assert notification.unread
    assert notification.recipient == post.user
    assert notification.actor == admin_user
    assert notification.action_object == post.comments.first()
