import pytest

from .factories import TitleFactory

pytestmark = pytest.mark.django_db


class TestTitle:
    def setup_method(self):
        self.title = TitleFactory()

    def test___str__(self):
        assert str(self.title) == self.title.word
