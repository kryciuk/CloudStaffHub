from django.test import tag
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status

from users.factories import CandidateFactory, OwnerFactory, EmployeeFactory
from organizations.factories import PositionFactory


class TestCityCreateView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_candidate = CandidateFactory.create()

    def test_if_candidate_cant_access_view(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("city-create"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_regular_employee_cant_access_view(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("city-create"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_owner_can_access_view(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("city-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("city-create"))
        self.assertTemplateUsed(response, "recruiter/city_create.html")


class TestPositionCreateView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_candidate = CandidateFactory.create()

    def test_if_candidate_cant_access_view(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("positions-create"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_regular_employee_cant_access_view(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("positions-create"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_owner_can_access_view(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("positions-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("positions-create"))
        self.assertTemplateUsed(response, "recruiter/positions_create.html")


class TestPositionDeleteView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.position = PositionFactory.create()

    def test_if_owner_can_delete_position(self):
        self.client.force_login(self.user_owner)
        response = self.client.post(reverse("positions-delete", kwargs={"pk": 1}), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_candidate_cant_delete_position(self):
        self.client.force_login(self.user_candidate)
        response = self.client.post(reverse("positions-delete", kwargs={"pk": 1}), follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_regular_employee_cant_delete_position(self):
        self.client.force_login(self.user_employee)
        response = self.client.post(reverse("positions-delete", kwargs={"pk": 1}), follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPositionListView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.positions = PositionFactory.create(company=self.user_owner.profile.company, title="Accountant")

    def test_if_owner_can_delete_position(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("positions-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_candidate_cant_delete_position(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("positions-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_regular_employee_cant_delete_position(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("positions-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_filtering_positions_works(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("positions-list"), data={"title": "Accountant"})
        self.assertEqual(len(response.context["positions"]), 1)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("positions-list"))
        self.assertTemplateUsed(response, "recruiter/positions_list.html")
