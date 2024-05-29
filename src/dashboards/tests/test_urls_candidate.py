from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class TestCandidateUrls(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user1", email="test_user1@test.com")
        self.user.set_password("password")
        self.user.save()

    def test_url_exists_at_correct_location(self):
        self.client.force_login(self.user)
        response = self.client.get("/dashboard/candidate/", {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_available_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard-candidate"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("dashboard-candidate"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
