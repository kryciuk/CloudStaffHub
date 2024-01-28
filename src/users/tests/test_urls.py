from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.factories import CandidateFactory, OwnerFactory


class TestUrls(TestCase):
    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()

    def test_authorization_urls_are_callable_by_name(self):
        response_register = self.client.get(reverse("register"))
        response_login = self.client.get(reverse("login"))
        self.assertEqual(response_register.status_code, status.HTTP_200_OK)
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

    def test_profiles_urls_are_callable_by_name_for_owner(self):
        self.client.force_login(self.user_owner)
        response_profile_view = self.client.get(reverse("profile", kwargs={"pk": self.user_owner.id}))
        response_profile_edit_for_owner = self.client.get(reverse("profile-edit", kwargs={"pk": self.user_owner.id}))
        self.assertEqual(response_profile_view.status_code, status.HTTP_200_OK)
        self.assertEqual(response_profile_edit_for_owner.status_code, status.HTTP_200_OK)

    def test_profiles_update_is_callable_by_name_for_candidate(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("profile-update", kwargs={"pk": self.user_candidate.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profiles_not_own_update_is_not_callable_by_name_for_candidate(self):
        self.client.force_login(self.user_candidate)
        response_profile_update_for_candidate = self.client.get(
            reverse("profile-update", kwargs={"pk": self.user_owner.id})
        )
        self.assertEqual(response_profile_update_for_candidate.status_code, status.HTTP_302_FOUND)

    def test_login_redirects_after_successful_login(self):
        response = self.client.post(reverse("login"), {"username": self.user_owner.username, "password": "password"})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
