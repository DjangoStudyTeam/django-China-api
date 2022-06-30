from datetime import timedelta

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test.utils import mail
from django.utils import timezone
from djoser import utils
from invitations.tests.factories import InvitationFactory
from test_plus.test import APITestCase
from titles.tests.factories import TitleFactory
from users.models import User


class AuthViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = self.make_user(username="user", password="password")
        self.user1 = self.make_user(username="u1", password="password")
        self.user1.is_active = False
        self.user1.save()

        self.invitation = InvitationFactory()

    def test_register(self):
        data = {
            "username": "another",
            "email": "another@example.com",
            "invitation_code": self.invitation.code,
            "password": "uncommon*pwd",
            "re_password": "uncommon*pwd",
        }
        response = self.post("api:auth-register", data=data)
        self.response_201(response)
        assert len(mail.outbox) == 1
        user = User.objects.get(username="another")
        assert not user.special
        assert user.titles.count() == 0
        self.invitation.refresh_from_db()
        assert self.invitation.invitee == user

    def test_register_with_special_and_titles_invitation(self):
        inv = InvitationFactory(special=True)

        title1 = TitleFactory()
        title2 = TitleFactory()
        inv.titles.add(title1, title2)

        data = {
            "username": "another",
            "email": "another@example.com",
            "invitation_code": inv.code,
            "password": "uncommon*pwd",
            "re_password": "uncommon*pwd",
        }
        response = self.post("api:auth-register", data=data)
        self.response_201(response)
        assert len(mail.outbox) == 1
        user = User.objects.get(username="another")
        assert user.special
        assert user.titles.count() == 2
        assert [title.word for title in user.titles.all()] == [title1.word, title2.word]
        inv.refresh_from_db()
        assert inv.invitee == user

    def test_register_with_invalid_invitation_code(self):
        data = {
            "username": "another",
            "email": "another@example.com",
            "invitation_code": "12344321",
            "password": "uncommon*pwd",
            "re_password": "uncommon*pwd",
        }
        response = self.post("api:auth-register", data=data)
        self.response_400(response)
        assert "invitation_code" in response.data

        invalid_inv = InvitationFactory(valid=False)
        data = {
            "username": "another",
            "email": "another@example.com",
            "invitation_code": invalid_inv.code,
            "password": "uncommon*pwd",
            "re_password": "uncommon*pwd",
        }
        response = self.post("api:auth-register", data=data)
        self.response_400(response)
        assert "invitation_code" in response.data

        expired_inv = InvitationFactory(expire_at=timezone.now() - timedelta(seconds=1))
        data = {
            "username": "another",
            "email": "another@example.com",
            "invitation_code": expired_inv.code,
            "password": "uncommon*pwd",
            "re_password": "uncommon*pwd",
        }
        response = self.post("api:auth-register", data=data)
        self.response_400(response)
        assert "invitation_code" in response.data

    def test_register_with_invalid_data(self):
        data = {
            "username": "another",
            "password": "uncommon*pwd",
            "invitation_code": "12344321",
        }
        response = self.post("api:auth-register", data=data)
        self.response_400(response)
        assert "re_password" in response.data
        assert "email" in response.data

    def test_register_with_existed_user(self):
        data = {
            "username": "user",
            "password": "uncommon*pwd",
            "invitation_code": self.invitation.code,
        }
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
        self.response_200(response)
        assert 200 == response.status_code

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
        self.response_200(response)
        assert 200 == response.status_code

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
        self.assertEqual(len(mail.outbox), 1)

    def test_forgot_password_with_invalid_data(self):
        data = {"email": "test@example.com"}
        response = self.post("api:auth-forgot_password", data=data)
        self.response_204(response)
        self.assertEqual(len(mail.outbox), 0)

    def test_reset_password(self):
        uid = utils.encode_uid(self.user.id)
        token = PasswordResetTokenGenerator().make_token(self.user)
        data = {"uid": uid, "token": token, "new_password": "uncommon*pwd", "re_new_password": "uncommon*pwd"}
        response = self.post("api:auth-reset_password", data=data)
        self.response_204(response)

    def test_reset_password_with_invalid_uid(self):
        data = {"uid": "1", "token": "abc123", "new_password": "uncommon*pwd", "re_new_password": "uncommon*pwd"}
        response = self.post("api:auth-reset_password", data=data)
        self.response_400(response)
        self.assertIn("uid", response.data)

    def test_reset_password_with_invalid_token(self):
        uid = utils.encode_uid(self.user.id)
        data = {"uid": uid, "token": "abc123", "new_password": "uncommon*pwd", "re_new_password": "uncommon*pwd"}
        response = self.post("api:auth-reset_password", data=data)
        self.response_400(response)
        self.assertIn("token", response.data)

    def test_reset_password_with_common_password(self):
        uid = utils.encode_uid(self.user.id)
        token = PasswordResetTokenGenerator().make_token(self.user)
        data = {"uid": uid, "token": token, "new_password": "admin123", "re_new_password": "admin123"}
        response = self.post("api:auth-reset_password", data=data)
        self.response_400(response)
        self.assertIn("new_password", response.data)

    def test_activate(self):
        self.user.is_active = False
        self.user.save()
        uid = utils.encode_uid(self.user.id)
        token = PasswordResetTokenGenerator().make_token(self.user)
        data = {"uid": uid, "token": token}
        response = self.post("api:auth-activate", data=data)
        self.response_200(response)
        assert 200 == response.status_code

    def test_activate_with_invalid_data(self):
        self.user.is_active = False
        self.user.save()
        uid = utils.encode_uid(self.user.id)
        token = PasswordResetTokenGenerator().make_token(self.user)
        data = {"uid": uid, "token": token}
        response = self.post("api:auth-activate", data=data)
        self.response_200(response)
        assert 200 == response.status_code

    def test_activate_with_is_active(self):
        uid = utils.encode_uid(self.user.id)
        token = PasswordResetTokenGenerator().make_token(self.user)
        data = {"uid": uid, "token": token}
        response = self.post("api:auth-activate", data=data)
        self.response_403(response)
        assert 403 == response.status_code

    def test_resend_activation(self):
        self.user.is_active = False
        self.user.save()
        data = {"email": "user@example.com"}
        response = self.post("api:auth-resend_activation", data=data)
        self.response_200(response)
        assert 200 == response.status_code

    def test_resend_activation_with_invalid_data(self):
        self.user.is_active = False
        self.user.save()
        data = {"email": "test@example.com"}
        response = self.post("api:auth-resend_activation", data=data)
        self.response_400(response)
        assert 400 == response.status_code

    def test_resend_activation_with_not_is_active(self):
        data = {"email": "user@example.com"}
        response = self.post("api:auth-resend_activation", data=data)
        self.response_400(response)
        assert 400 == response.status_code
