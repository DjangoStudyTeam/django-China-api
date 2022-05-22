from actstream.models import Action, Follow
from comments.models import Comment
from posts.tests.factories import PostFactory
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from test_plus.test import APITestCase
from tree_comments.serializers import TreeCommentListWithParentUserSerializer


class CommentListNestedViewSetTestCase(APITestCase):
    def setUp(self):
        self.api_request_factory = APIRequestFactory()
        self.user = self.make_user(username="user", password="password")
        self.post1 = PostFactory(user=self.user)

        self.comment_1a = Comment.objects.create(content="test comment 1a", post=self.post1, user=self.user)
        self.comment_1aa = Comment.objects.create(content="test comment 1aa", post=self.post1, user=self.user)
        self.comment_1aaa = Comment.objects.create(content="test comment 1aaa", post=self.post1, user=self.user)
        self.comment_1b = Comment.objects.create(content="test comment 1b", post=self.post1, user=self.user)
        self.comment_1c = Comment.objects.create(content="test comment 1c", post=self.post1, user=self.user)
        self.comment_1cc = Comment.objects.create(content="test comment 1cc", post=self.post1, user=self.user)

        self.post2 = PostFactory(user=self.user)
        self.comment_2a = Comment.objects.create(content="test comment 2a", post=self.post2, user=self.user)
        self.comment_2b = Comment.objects.create(content="test comment 2b", post=self.post2, user=self.user)
        self.comment_2bb = Comment.objects.create(content="test comment 2bb", post=self.post2, user=self.user)

        self.list_url1 = self.reverse("api:posts-comment-list", post_id=self.post1.id)
        self.list_url2 = self.reverse("api:posts-comment-list", post_id=self.post2.id)

    def test_permission(self):
        response = self.client.get(self.list_url1)
        self.response_200(response)

    def test_list(self):
        response = self.client.get(self.list_url1)
        self.response_200(response)

        request = self.api_request_factory.get(self.list_url1)
        serializer = TreeCommentListWithParentUserSerializer(
            instance=[
                self.comment_1a,
                self.comment_1aa,
                self.comment_1aaa,
                self.comment_1b,
                self.comment_1c,
                self.comment_1cc,
            ],
            many=True,
            context={"request": Request(request)},
        )
        self.assertEqual(response.data["results"], serializer.data)

        request = self.api_request_factory.get(self.list_url2)
        response = self.client.get(self.list_url2)
        self.response_200(response)
        serializer = TreeCommentListWithParentUserSerializer(
            instance=[
                self.comment_2a,
                self.comment_2b,
                self.comment_2bb,
            ],
            many=True,
            context={"request": Request(request)},
        )
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_like_permission(self):
        # anonymous
        response = self.post("api:comment-like", pk=self.comment_1a.pk)
        self.response_401(response)

        # authenticated
        self.login(username=self.user.username, password="password")
        response = self.post("api:comment-like", pk=self.comment_1a.pk)
        self.response_201(response)

    def test_create_like(self):
        self.login(username=self.user.username, password="password")
        response = self.post("api:comment-like", pk=self.comment_1a.pk)
        self.response_201(response)

        assert Follow.objects.count() == 1
        like_obj = Follow.objects.get()
        assert like_obj.user == self.user
        assert like_obj.flag == "like"
        assert like_obj.follow_object == self.comment_1a

        assert Action.objects.count() == 1
        action_obj = Action.objects.get()
        assert action_obj.actor == self.user
        assert action_obj.verb == "like"
        assert action_obj.target == self.comment_1a

    def test_create_like_twice(self):
        self.login(username=self.user.username, password="password")
        response = self.post("api:comment-like", pk=self.comment_1a.pk)
        self.response_201(response)

        response = self.post("api:comment-like", pk=self.comment_1a.pk)
        self.response_201(response)

        assert Follow.objects.count() == 1
        assert Action.objects.count() == 1

    def test_create_like_with_nonexistent_comment(self):
        self.login(username=self.user.username, password="password")
        response = self.post("api:comment-like", pk=9999)
        self.response_404(response)


class CommentCreateUpdateViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = self.make_user(username="user", password="password")
        self.post = PostFactory(user=self.user)
        self.comment = Comment.objects.create(content="test comment", post=self.post, user=self.user)

        self.list_url = self.reverse("api:comment-list")
        self.detail_url = self.reverse("api:comment-detail", pk=self.comment.pk)

    def test_permission(self):
        response = self.client.post(self.list_url, data={})
        self.response_401(response)

        response = self.client.patch(self.detail_url, data={})
        self.response_401(response)

    def test_create(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.post(
            self.list_url, data={"post": self.post.id, "content": "comment content from test create"}
        )
        self.response_201(response)

    def test_create_with_invalid_data(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.post(self.list_url, data={"post": self.post.id})
        self.response_400(response)
        self.assertIn("content", response.data)

    def test_update(self):
        self.client.login(username=self.user.username, password="password")
        new_content = "updated comment content"
        response = self.client.patch(self.detail_url, data={"content": new_content})
        self.response_200(response)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, new_content)

    def test_update_with_invalid_data(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.patch(self.detail_url, data={"content": ""})
        self.response_400(response)
        self.assertIn("content", response.data)

    def test_update_nonexistent_comment(self):
        self.client.login(username=self.user.username, password="password")
        url = self.reverse("api:comment-detail", pk=999999)
        response = self.client.patch(url, data={"content": "updated comment content"})
        self.response_404(response)
