import pytest
from invitations.tests.factories import InvitationFactory
from rest_framework import serializers
from users.serializers import RegisterSerializer

pytestmark = pytest.mark.django_db


class TestRegisterSerializer:
    def test_perform_create_no_updated_rows(self):
        serializer = RegisterSerializer()
        with pytest.raises(serializers.ValidationError):
            serializer.perform_create({"invitation": InvitationFactory(valid=False)})
