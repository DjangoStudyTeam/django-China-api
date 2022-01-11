import factory
from factory import Faker
from factory.django import DjangoModelFactory, ImageField
from nodes.models import Node


class NodeFactory(DjangoModelFactory):
    class Meta:
        model = Node

    name = factory.Sequence(lambda n: "name%d" % n)
    slug = factory.Sequence(lambda n: "slug%d" % n)
    cover = ImageField()
    description = Faker("text")
