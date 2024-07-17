from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
from django.urls import reverse


class TestEmployeeViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client(HTTP_HOST="localhost:8000")

        user = User.objects.create(username="test_user1", email="test_user1@test.com")
        user.set_password("password")
        user.save()

        employee, _ = Group.objects.get_or_create(name="Employee")
        employee.user_set.add(user)

        cls.user = user

    def test_template_name_correct(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(reverse("dashboard-employee"), {"user_id": self.user.id})
        self.assertTemplateUsed(response, "dashboards/dashboard_employee.html")
