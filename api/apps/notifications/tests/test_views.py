from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from posts.tests.factories import PostFactory
from test_plus.test import APITestCase


class NotificationViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = self.make_user(username="user", password="password")
        self.user2 = self.make_user(username="user2", password="password")
        self.list_url = self.reverse("api:comment-list")
        self.post = PostFactory(user=self.user)

    def test_notification(self):
        self.client.login(username=self.user2.username, password="password")
        response = self.client.post(
            self.list_url, data={"post": self.post.id, "content": "comment content from test create a notification"}
        )
        self.response_201(response)
        actor_id = Comment.objects.get(pk=response.data["id"]).user_id
        notification = Notification.objects.get(actor_id=actor_id)
        assert notification.content == ""
        assert notification.unread == 1
        assert int(notification.action_object_object_id) == response.data["id"]
        assert notification.action_object_content_type_id == ContentType.objects.get_for_model(Comment).id
        assert notification.actor_id == self.user2.id
        assert notification.recipient_id == self.post.user_id
