import time

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test.utils import mail
from djoser import utils
from test_plus.test import APITestCase
from .factories import UserFactory


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

    def test_logout(self):
        data = {"username": "user", "password": "password"}
        authorization = "token " + self.post("api:auth-login", data=data).data["key"]
        response = self.post("api:auth-logout", extra={"HTTP_AUTHORIZATION": authorization})
        self.response_204(response)
        assert 204 == response.status_code

    def test_logout_with_no_authentication(self):
        response = self.post("api:auth-logout")
        self.response_401(response)
        assert "Unauthorized" in response.status_text

    def test_logout_with_authentication_invalid_data(self):
        response = self.post("api:auth-logout", extra={"HTTP_AUTHORIZATION": "token abc123"})
        self.response_401(response)
        assert "Unauthorized" in response.status_text

    def test_change_password(self):
        data = {"username": "user", "password": "password"}
        authorization = "token " + self.post("api:auth-login", data=data).data["key"]
        data = {"current_password": "password", "new_password": "admin777", "re_new_password": "admin777"}
        response = self.post("api:auth-change_password", data=data, extra={"HTTP_AUTHORIZATION": authorization})
        self.response_204(response)
        assert 204 == response.status_code

    def test_change_password_with_invalid_data(self):
        data = {"username": "user", "password": "password"}
        authorization = "token " + self.post("api:auth-login", data=data).data["key"]
        data = {"current_password": "password", "new_password": "admin777", "re_new_password": "admin776"}
        response = self.post("api:auth-change_password", data=data, extra={"HTTP_AUTHORIZATION": authorization})
        self.response_400(response)
        assert "non_field_errors" in response.data

    def test_forgot_password(self):
        data = {"email": "user@example.com"}
        response = self.post("api:auth-forgot_password", data=data)
        self.response_204(response)
        assert 204 == response.status_code

    def test_forgot_password_with_invalid_data(self):
        data = {"email": "test@example.com"}
        response = self.post("api:auth-forgot_password", data=data)
        self.response_400(response)
        assert "email_not_found" in response.data

    def test_reset_password(self):
        data = {"username": "user", "password": "password"}
        key = self.post("api:auth-login", data=data).data["key"]
        uid = utils.encode_uid(self.user.id)
        token = PasswordResetTokenGenerator().make_token(self.user.username)
        authorization = "token " + key
        data = {
            "uid": uid,
            "token": token,
            "new_password": "password1",
            "re_new_password": "password1",
            "current_password": "password"
        }
        response = self.post("api:auth-reset_password", data=data, extra={"HTTP_AUTHORIZATION": authorization})
        self.response_204(response)
        assert 204 == response.status_code
