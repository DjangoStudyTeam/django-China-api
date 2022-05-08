import factory
from comments.models import Comment
from factory import Faker
from factory.django import DjangoModelFactory
from posts.tests.factories import PostFactory
from users.tests.factories import UserFactory

factory.Faker.override_default_locale("en_US")


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    content = Faker("sentence")
    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
