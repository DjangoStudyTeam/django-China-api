import factory
from factory import Faker
from factory.django import DjangoModelFactory
from nodes.tests.factories import NodeFactory
from posts.models import Post
from users.tests.factories import UserFactory

factory.Faker.override_default_locale("en_US")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    body = Faker("word")
    title = Faker("word")
    views = Faker("random_digit")
    pinned = Faker("boolean")
    highlighted = Faker("boolean")
    deleted = False
    node = factory.SubFactory(NodeFactory)
    user = factory.SubFactory(UserFactory)
