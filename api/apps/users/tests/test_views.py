from django.test.utils import mail
from test_plus.test import APITestCase


class AuthViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = self.make_user(username="user", password="password")
        self.user1 = self.make_user(username="u1", password="password")
        self.user1.is_active = False
        self.user1.save()

    def test_register(self):
        data = {
            "username": "another",
            "email": "another@example.com",
            "password": "uncommon*pwd",
            "re_password": "uncommon*pwd",
        }
        response = self.post("api:auth-register", data=data)
        self.response_201(response)
        assert len(mail.outbox) == 1

    def test_register_with_invalid_data(self):
        data = {"username": "another", "password": "uncommon*pwd"}
        response = self.post("api:auth-register", data=data)
        self.response_400(response)
        assert "re_password" in response.data
        assert "email" in response.data

    def test_register_with_existed_user(self):
        data = {"username": "user", "password": "uncommon*pwd"}
        response = self.post("api:auth-register", data=data)
        self.response_400(response)
        assert "username" in response.data

    def test_login(self):
        data = {"username": "user", "password": "password"}
        response = self.post("api:auth-login", data=data)
        self.response_200(response)
        assert "user" in response.data

    def test_login_with_invalid_data(self):
        data = {"username": "user", "password": "uncommon*pwd"}
        response = self.post("api:auth-login", data=data)
        self.response_400(response)
        assert "non_field_errors" in response.data

    def test_login_with_unregistered_user(self):
        data = {"username": "another", "password": "password"}
        response = self.post("api:auth-login", data=data)
        self.response_400(response)
        assert "non_field_errors" in response.data

    def test_login_with_not_active_user(self):
        data = {"username": "u1", "password": "password"}
        response = self.post("api:auth-login", data=data)
        self.response_400(response)
        assert "non_field_errors" in response.data
