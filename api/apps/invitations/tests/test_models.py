from unittest.mock import MagicMock

import pytest
from django.utils import timezone
from invitations.models import Invitation

from .factories import InvitationFactory

pytestmark = pytest.mark.django_db


class TestInvitation:
    def setup_method(self):
        self.invitation = InvitationFactory(code="12345678")
        self.expired_invitation = InvitationFactory(expire_at=timezone.now())

    def test___str__(self):
        assert str(self.invitation) == "12345678"

    def test_save(self):
        invitation = Invitation()
        invitation.save()
        invitation.refresh_from_db(fields=["code"])
        assert len(invitation.code) == Invitation.CODE_LENGTH

    def test_expired(self):
        invitation = Invitation()
        assert not invitation.expired()
        assert self.expired_invitation.expired()

    def test_gen_code(self, monkeypatch):
        monkeypatch.setattr(
            "invitations.models.get_random_string",
            MagicMock(side_effect=["12345678", "23456789"]),
        )
        assert Invitation.gen_code() == "23456789"
