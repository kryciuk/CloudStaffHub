from django.test import SimpleTestCase
from django.urls import resolve, reverse


class TestUrls(SimpleTestCase):
    def test_list_url_is_resolved(self):
        assert 1 == 2
