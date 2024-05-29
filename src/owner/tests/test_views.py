from django.contrib.auth.models import Group
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status

from organizations.factories import DepartmentFactory
from organizations.models import Department
from users.factories import EmployeeFactory, OwnerFactory


class TestDepartmentCreateView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_manager = EmployeeFactory.create()
        self.user_manager.groups.clear()
        manager_group = Group.objects.get(name="Manager")
        manager_group.user_set.add(self.user_manager)
        self.user_manager.profile.company = self.user_owner.profile.company
        self.user_manager.profile.save()
        self.user_employee = EmployeeFactory.create()

    def test_if_owner_can_access_view(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("department-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_manager_cant_access_view_and_is_redirected_to_correct_dashboard(self):
        self.client.force_login(self.user_manager)
        response = self.client.get(reverse("department-create"), follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(response, reverse("dashboard-manager"))
        self.assertEqual(message.message, "You don't have the required permissions to access this page.")

    def test_if_employee_cant_access_view_and_is_redirected_to_correct_dashboard(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("department-create"), follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(response, reverse("dashboard-employee"))
        self.assertEqual(message.message, "You don't have the required permissions to access this page.")

    def test_if_only_managers_from_company_are_possible_choice(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("department-create"))
        self.assertEqual(len(response.context["form"].fields["manager"].queryset), 1)

    def test_if_title_is_correct(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("department-create"))
        title = response.context["title"]
        self.assertEqual(title, "Create Department - CloudStaffHub")

    def test_if_correct_template_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("department-create"))
        self.assertTemplateUsed(response, "owner/department_create.html")


class TestDepartmentDeleteView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        Department.objects.all().delete()
        self.user_owner = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.department = DepartmentFactory.create(company=self.user_owner.profile.company)

    def test_if_owner_can_delete_department(self):
        self.client.force_login(self.user_owner)
        response = self.client.post(reverse("department-delete", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Department.objects.count(), 0)

    def test_if_employee_cant_delete_department(self):
        self.client.force_login(self.user_employee)
        response = self.client.post(reverse("department-delete", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Department.objects.count(), 1)


class TestDepartmentListView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        Department.objects.all().delete()
        self.user_owner = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.department = DepartmentFactory.create_batch(5, company=self.user_owner.profile.company)

    def test_if_owner_can_view_departments_list(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("department-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context["departments"]), 5)

    def test_if_employee_cant_view_departments_list(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("department-list"), follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(message.message, "You don't have the required permissions to access this page.")

    def test_if_title_is_correct(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("department-list"))
        title = response.context["title"]
        self.assertEqual(title, "Departments - CloudStaffHub")

    def test_if_correct_template_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("department-list"))
        self.assertTemplateUsed(response, "owner/department_list.html")
