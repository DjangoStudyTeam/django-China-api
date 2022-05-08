from datetime import timedelta

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from invitations.models import Invitation
from users.tests.factories import UserFactory


class InvitationFactory(DjangoModelFactory):
    class Meta:
        model = Invitation

    expire_at = factory.LazyFunction(lambda: timezone.now() + timedelta(days=30))
    creator = factory.SubFactory(UserFactory)
