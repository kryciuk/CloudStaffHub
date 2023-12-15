from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status


class TestEmployeeUrls(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client(HTTP_HOST="localhost:8000")

        user = User.objects.create(username="test_user1", email="test_user1@test.com")
        user.set_password("password")
        user.save()

        user_not_employee = User.objects.create(username="test_user2", email="test_user2@test.com")
        user_not_employee.set_password("password")
        user_not_employee.save()

        employee, _ = Group.objects.get_or_create(name="Employee")
        employee.user_set.add(user)

        cls.user = user
        cls.user_not_employee = user_not_employee

    # def test_url_exists_at_correct_location_if_user_has_group_employee(self):
    #     self.client.login(username=self.user.username, password="password")
    #     response = self.client.get("dashboard/employee/", {"user_id": self.user.id})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_available_by_name_if_user_has_group_employee(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(reverse("dashboard-employee"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_forbidden_if_user_is_not_employee(self):
        self.client.login(username=self.user_not_employee.username, password="password")
        response = self.client.get(reverse("dashboard-employee"), {"user_id": self.user_not_employee.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_url_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("dashboard-employee"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
