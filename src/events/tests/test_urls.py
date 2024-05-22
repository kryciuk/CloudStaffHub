from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status

from users.factories import CandidateFactory, OwnerFactory


class TestUrls(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_candidate = CandidateFactory.create()
        self.user_owner = OwnerFactory.create()
        self.urls = {
            "calendar": reverse("calendar", kwargs={"year": 2025, "month_number": 12}),
            "assignments": reverse("assignments"),
            "assignments-create": reverse("assignments-create"),
        }

    def test_positions_and_city_urls_are_callable_by_name_for_owner(self):
        self.client.force_login(self.user_owner)
        for name, url in self.urls.items():
            with self.subTest(url_name=name):
                res = self.client.get(url)
                self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_positions_and_city_urls_are_unavailable_for_candidate(self):
        self.client.force_login(self.user_candidate)
        for name, url in self.urls.items():
            with self.subTest(url_name=name):
                res = self.client.get(url)
                self.assertEqual(res.status_code, status.HTTP_302_FOUND)
