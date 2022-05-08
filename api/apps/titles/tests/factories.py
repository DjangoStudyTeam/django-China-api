import factory
from factory import Faker
from factory.django import DjangoModelFactory
from titles.models import Title

factory.Faker.override_default_locale("en_US")


class TitleFactory(DjangoModelFactory):
    class Meta:
        model = Title

    word = Faker("word")
