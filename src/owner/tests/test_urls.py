from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from organizations.factories import DepartmentFactory
from users.factories import CandidateFactory, EmployeeFactory, OwnerFactory


class TestUrls(TestCase):
    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.department = DepartmentFactory.create(company=self.user_owner.profile.company)
        self.urls1 = {
            "department-create": reverse("department-create"),
            "department-list": reverse("department-list"),
        }
        self.urls2 = {"department-delete": reverse("department-delete", kwargs={"pk": self.department.id})}

    def test_polls_urls_are_callable_by_name_for_owner(self):
        self.client.force_login(self.user_owner)
        for name, url in self.urls1.items():
            with self.subTest(url_name=name):
                res = self.client.get(url)
                self.assertEqual(res.status_code, status.HTTP_200_OK)
        for name, url in self.urls2.items():
            with self.subTest(url_name=name):
                res = self.client.post(url)
                self.assertEqual(res.status_code, status.HTTP_302_FOUND)

    def test_polls_urls_are_redirecting_for_candidate(self):
        self.client.force_login(self.user_candidate)
        for name, url in self.urls1.items():
            with self.subTest(url_name=name):
                res = self.client.get(url)
                self.assertEqual(res.status_code, status.HTTP_302_FOUND)

    def test_polls_urls_delete_is_forbidden_for_candidate(self):
        self.client.force_login(self.user_candidate)
        res = self.client.get(self.urls2["department-delete"])
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_polls_urls_are_redirecting_for_regular_employee(self):
        self.client.force_login(self.user_employee)
        for name, url in self.urls1.items():
            with self.subTest(url_name=name):
                res = self.client.get(url)
                self.assertEqual(res.status_code, status.HTTP_302_FOUND)

    def test_polls_urls_delete_if_forbidden_for_regular_employee(self):
        self.client.force_login(self.user_employee)
        res = self.client.get(self.urls2["department-delete"])
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
