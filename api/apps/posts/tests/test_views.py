from django.contrib.auth import get_user_model
from nodes.tests.factories import NodeFactory
from test_plus.test import APITestCase

from .factories import PostFactory

User = get_user_model()


class PostViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(username="admin", password="password", email="admin@gmail.com")
        self.normal_user = self.make_user(username="normal", password="password")
        self.posts_list_url = self.reverse("api:posts-list")
        self.nonexistent_posts_detail_url = self.reverse("api:posts-detail", pk=9999999)

    def test_list_permission(self):
        # anonymous
        response = self.get(self.posts_list_url)
        self.response_200(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get(self.posts_list_url)
        self.response_200(response)

    def test_list_posts(self):
        PostFactory.create_batch(5)
        response = self.get(self.posts_list_url)
        for i in response.data:
            assert 1 == i["views"]
        assert 200 == response.status_code

    def test_retrieve_permission(self):
        posts = PostFactory()

        # anonymous user
        response = self.get("api:posts-detail", pk=posts.pk)
        self.response_200(response)

        # normal user
        self.login(username=self.normal_user.username, password="password")
        response = self.get("api:posts-detail", pk=posts.pk)
        self.response_200(response)

    def test_retrieve_nonexistent_posts(self):
        response = self.get(self.nonexistent_posts_detail_url)
        self.response_404(response)

    def test_retrieve_posts(self):
        posts = PostFactory()
        response = self.get("api:posts-detail", pk=posts.pk)
        self.response_200(response)
        assert 1 == response.data["views"]

    def test_create_permission(self):
        # anonymous
        response = self.post(self.posts_list_url)
        self.response_401(response)

    def test_create_posts(self):
        node = NodeFactory()
        data = {"title": "test", "body": "test", "node": node.pk}
        self.login(username=self.normal_user.username, password="password")
        response = self.post(self.posts_list_url, data=data)
        self.response_201(response)
        assert response.data["user"] == "normal"

    def test_create_posts_with_invalid_data(self):
        data = {"title": "", "body": "", "node": 99, "user": 99}
        self.login(username=self.normal_user.username, password="password")
        response = self.post(self.posts_list_url, data=data)
        self.response_400(response)
        assert "title" in response.data

    def test_patch_posts(self):
        self.test_create_posts()
        data = {"title": "123"}
        self.login(username=self.normal_user.username, password="password")
        response = self.patch("api:posts-detail", pk=1, data=data)
        self.response_200(response)
        assert response.data["title"] == "123"

    def test_patch_nonexistent_posts(self):
        self.login(username=self.normal_user.username, password="password")
        response = self.patch(self.nonexistent_posts_detail_url)
        self.response_404(response)

    def test_patch_posts_with_invalid_data(self):
        self.test_create_posts()
        data = {"node": 99}
        self.login(username=self.normal_user.username, password="password")
        response = self.patch("api:posts-detail", pk=1, data=data)
        self.response_400(response)
        assert "node" in response.data

    def test_patch_permission(self):
        # anonymous
        response = self.patch("api:posts-detail", pk=1)
        self.response_401(response)

        # other_user
        posts = PostFactory()
        data = {"title": "123"}
        self.login(username=self.normal_user.username, password="password")
        response = self.patch("api:posts-detail", pk=posts.pk, data=data)
        self.response_403(response)
