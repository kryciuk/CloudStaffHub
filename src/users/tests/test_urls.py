from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .setup_for_tests import setUp_for_tests


class TestUrls(TestCase):
    def setUp(self):
        self.user_owner, self.user_candidate = setUp_for_tests()

    def test_authorization_urls_are_callable_by_name(self):
        response_register = self.client.get(reverse("register"))
        response_login = self.client.get(reverse("login"))
        response_logout = self.client.get(reverse("logout"))
        self.assertEqual(response_register.status_code, status.HTTP_200_OK)
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)

    def test_profiles_urls_are_callable_by_name_for_owner(self):
        self.client.force_login(self.user_owner)
        response_profile_view = self.client.get(reverse("profile", kwargs={"pk": self.user_owner.id}))
        response_profile_edit_for_owner = self.client.get(reverse("profile-edit", kwargs={"pk": self.user_owner.id}))
        self.assertEqual(response_profile_view.status_code, status.HTTP_200_OK)
        self.assertEqual(response_profile_edit_for_owner.status_code, status.HTTP_200_OK)

    def test_profiles_urls_are_callable_by_name_for_candidate(self):
        self.client.force_login(self.user_candidate)
        response_profile_edit_for_candidate = self.client.get(
            reverse("profile-update", kwargs={"pk": self.user_candidate.id}))
        self.assertEqual(response_profile_edit_for_candidate.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_redirects_after_successful_login(self):
        response = self.client.post(reverse("login"), {"username": self.user_owner.username, "password": "password"})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
