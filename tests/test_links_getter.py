from unittest import TestCase
from parser import Nemez1da_parser
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class TestLinksGetter(TestCase):
    def setUp(self):
        self.links = Nemez1da_parser.LinksGetter().get_links()
        self.validator = URLValidator()

    def test_links(self):
        for link in self.links:
            try:
                self.validator(link)
            except (ValidationError,) as e:
                self.fail(e)
