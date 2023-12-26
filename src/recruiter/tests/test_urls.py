from django.test import TransactionTestCase, tag
from django.urls import resolve, reverse
from rest_framework import status

from organizations.factories import PositionFactory, DepartmentFactory
from users.factories import CandidateFactory, OwnerFactory


class TestUrls(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_candidate = CandidateFactory.create()
        self.user_owner = OwnerFactory.create()
        department = DepartmentFactory.create(company=self.user_owner.profile.company)
        position = PositionFactory.create(department=department)
        self.urls = {
            "positions-create": reverse("positions-create"),
            "positions-list": reverse("positions-list"),
            "city-create": reverse("city-create")
        }

    def test_positions_and_city_urls_are_callable_by_name_for_owner(self):
        self.client.force_login(self.user_owner)
        for name, url in self.urls.items():
            with self.subTest(url_name=name):
                res = self.client.get(url)
                self.assertEqual(
                    res.status_code, status.HTTP_200_OK
                )
        response = self.client.post(reverse("positions-delete", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_positions_and_city_urls_are_forbidden_for_candidate(self):
        self.client.force_login(self.user_candidate)
        urls = {
            "positions-create": reverse("positions-create"),
            "positions-list": reverse("positions-list"),
            "city-create": reverse("city-create")
        }
        for name, url in self.urls.items():
            with self.subTest(url_name=name):
                res = self.client.get(url)
                self.assertEqual(
                    res.status_code, status.HTTP_403_FORBIDDEN
                )
        response = self.client.post(reverse("positions-delete", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)