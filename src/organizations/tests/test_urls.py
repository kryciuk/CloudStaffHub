from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.factories import OwnerFactory


class TestUrls(TestCase):
    def setUp(self):
        self.user_owner = OwnerFactory()
        self.urls = {
            "register-company": reverse("register-company"),
            "company-profile": reverse("company-profile", kwargs={"pk": self.user_owner.profile.company.id}),
        }

    def test_polls_urls_are_callable_by_name(self):
        response = self.client.get(self.urls["register-company"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_login(self.user_owner)
        response = self.client.get(self.urls["company-profile"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
