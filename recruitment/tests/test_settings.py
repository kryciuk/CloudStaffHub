from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.test import SimpleTestCase


class TestSettings(SimpleTestCase):
    def test_secret_key_strength(self):
        validate_password(settings.SECRET_KEY)
