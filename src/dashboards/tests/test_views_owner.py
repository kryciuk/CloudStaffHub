from django.contrib.auth.models import Group, User
from django.test import Client, TestCase, tag
from django.urls import reverse
from rest_framework import status


class TestCandidateViews(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user1", email="test_user1@test.com")
        self.user.set_password("password")
        self.user.save()

        creator, _ = Group.objects.get_or_create(name="Creator")
        creator.user_set.add(self.user)

    def test_template_name_correct(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard-owner"), {"user_id": self.user.id})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "dashboards/dashboard_owner.html")

    def test_cant_access_view_without_creator_group(self):
        user_1 = User.objects.create(username="test_user2", email="test_user1@test.com")
        user_1.set_password("password")
        user_1.save()
        self.client.force_login(user_1)
        response = self.client.get(reverse("dashboard-owner"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
