from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.factories import CandidateFactory, OwnerFactory


class TestOwnerViews(TestCase):
    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()

    def test_template_name_correct(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("dashboard-owner"), {"user_id": self.user_owner.id})
        self.assertTemplateUsed(response, "dashboards/dashboard_owner.html")

    def test_cant_access_view_without_creator_group(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("dashboard-owner"), {"user_id": self.user_candidate.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
