from test_plus.test import APITestCase


class PostsViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = self.make_user(username="user", password="password")

    def get_token(self):
        data = {"username": "user", "password": "password"}
        authorization = "token " + self.post("api:auth-login", data=data).data["key"]
        return authorization

    # node接口未开发完成，不知道怎么创建数据
    # def test_add_posts(self):
    #     data = {"title": "test1", "body": "1", "views": 1, "user": 1, "node": 1}
    #     authorization = self.get_token()
    #     response = self.post("api:posts", data=data, extra={"HTTP_AUTHORIZATION": authorization})
    #     self.response_201(response)

    def test_add_posts_no_exist_node(self):
        data = {"title": "test1", "body": "1", "views": 1, "user": 1, "node": 1}
        authorization = self.get_token()
        response = self.post(
            "http://localhost:8000/api/v1/posts/", data=data, extra={"HTTP_AUTHORIZATION": authorization}
        )
        self.response_400(response)
        assert "node" in response.data
