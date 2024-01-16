from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.factories import CandidateFactory, OwnerFactory


class TestOwnerUrls(TestCase):
    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()

    def test_url_exists_at_correct_location_if_user_has_group_owner(self):
        self.client.force_login(self.user_owner)
        response = self.client.get("/dashboard/owner/", {"user_id": self.user_owner.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_available_by_name_if_user_has_group_creator(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("dashboard-owner"), {"user_id": self.user_owner.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_forbidden_if_user_is_not_creator(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("dashboard-owner"), {"user_id": self.user_candidate.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_url_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("dashboard-owner"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
