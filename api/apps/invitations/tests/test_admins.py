import pytest
from django.urls import reverse
from invitations.models import Invitation

pytestmark = pytest.mark.django_db


def test_auto_set_admin_as_invitation_creator(admin_client, admin_user):
    url = reverse("admin:invitations_invitation_add")
    response = admin_client.post(url)
    assert response.status_code == 302

    assert Invitation.objects.count() == 1
    inv = Invitation.objects.get()
    assert inv.creator == admin_user
