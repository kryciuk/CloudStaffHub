import datetime as dt

from django.test import TransactionTestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from events.factories import AssignmentFactory
from events.models import Assignment
from users.factories import CandidateFactory, EmployeeFactory, OwnerFactory


class TestAssignmentCreateView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.user_employee.profile.company = self.user_owner.profile.company
        self.user_employee.profile.save()
        self.data = {
            "name": "Test",
            "description": "Test description",
            "event_date": timezone.datetime(2026, 10, 12, tzinfo=dt.timezone.utc),
            "employee": [self.user_owner],
        }

    def test_if_candidate_cant_access_view_and_is_redirected_to_correct_dashboard(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("assignments-create"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("dashboard-candidate"))

    def test_if_employee_can_access_view(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("assignments-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_message_is_shown_if_access_to_view_is_denied(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("assignments-create"), follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.message, "You don't have the required permissions to access this page.")

    def test_if_owner_can_access_view(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("assignments-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # @tag("y")
    # def test_if_owner_can_create_assignment(self):
    #     self.client.force_login(self.user_owner)
    #     response = self.client.post(
    #         reverse("assignments-create"), data=self.data)
    #     print(response.context.get("messages"))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Assignment.objects.count(), 1)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("assignments-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "events/assignments/assignment_create.html")


class TestAssignmentListView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        # candidate
        self.user_candidate = CandidateFactory.create()

        # company1
        self.user_owner1 = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_employee.profile.company = self.user_owner1.profile.company
        self.user_employee.profile.save()
        self.assignment1 = AssignmentFactory.create(manager=self.user_owner1, status=False)
        self.assignment1.employee.set([self.user_employee])
        self.assignment1.save()
        self.assignment3 = AssignmentFactory.create(status=False)
        self.assignment3.employee.set([self.user_employee])
        self.assignment3.save()

        # company2
        self.user_owner2 = OwnerFactory.create()
        self.assignment2 = AssignmentFactory.create(manager=self.user_owner2, status=False)
        self.assignment2.employee.set([self.user_owner2])
        self.assignment2.save()

    def test_if_candidate_cant_access_view_and_is_redirected_to_correct_dashboard(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("assignments"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("dashboard-candidate"))

    def test_if_employee_can_access_view(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("assignments"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_message_is_shown_if_access_to_view_is_denied(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("assignments"), follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.message, "You don't have the required permissions to access this page.")

    def test_if_owner_can_access_view(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("assignments"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("assignments"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "events/assignments/assignment_list.html")

    def test_if_user_sees_only_own_assignments(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("assignments"))
        self.assertEqual(
            len(response.context["object_list"]), len(Assignment.objects.filter(employee=self.user_employee).all())
        )
        self.client.force_login(self.user_employee)
        self.client.logout()
        self.client.force_login(self.user_owner2)
        response = self.client.get(reverse("assignments"))
        self.assertEqual(
            len(response.context["object_list"]), len(Assignment.objects.filter(employee=self.user_owner2).all())
        )

    def test_if_user_can_close_assignment(self):
        self.client.force_login(self.user_employee)
        response = self.client.post(reverse("assignments-close", kwargs={"pk": self.assignment1.id}), follow=True)
        self.assignment1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.assignment1.status)

    def test_if_message_is_shown_after_closing_assignment(self):
        self.client.force_login(self.user_employee)
        response = self.client.post(reverse("assignments-close", kwargs={"pk": self.assignment1.id}), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.message, "Assignment is now closed.")


class TestCalendarView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        # candidate
        self.user_candidate = CandidateFactory.create()

        # company1
        self.user_owner1 = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_employee.profile.company = self.user_owner1.profile.company
        self.user_employee.profile.save()
        self.assignments = AssignmentFactory.create_batch(
            5, manager=self.user_owner1, status=False, event_date=timezone.now() + timezone.timedelta(seconds=1)
        )
        self.assignments_next_month = AssignmentFactory.create_batch(
            4, manager=self.user_owner1, status=False, event_date=timezone.now() + timezone.timedelta(days=30)
        )
        for assignment in self.assignments:
            assignment.employee.set([self.user_employee])
            assignment.save()
        for assignment in self.assignments_next_month:
            assignment.employee.set([self.user_employee])
            assignment.save()

    def test_if_employee_can_see_assignments_in_correct_month(self):
        self.client.force_login(self.user_employee)
        now_month = timezone.now().month
        now_year = timezone.now().year
        response = self.client.get(reverse("calendar", kwargs={"year": now_year, "month_number": now_month}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context["assignments"]), 5)
        response = self.client.get(reverse("calendar", kwargs={"year": now_year, "month_number": now_month + 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context["assignments"]), 4)

    def test_if_candidate_cant_access_view_and_is_redirected_to_correct_dashboard(self):
        self.client.force_login(self.user_candidate)
        now_month = timezone.now().month
        now_year = timezone.now().year
        response = self.client.get(reverse("calendar", kwargs={"year": now_year, "month_number": now_month}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("dashboard-candidate"))

    def test_if_employee_can_access_view(self):
        self.client.force_login(self.user_employee)
        now_month = timezone.now().month
        now_year = timezone.now().year
        response = self.client.get(reverse("calendar", kwargs={"year": now_year, "month_number": now_month}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_message_is_shown_if_access_to_view_is_denied(self):
        self.client.force_login(self.user_candidate)
        now_month = timezone.now().month
        now_year = timezone.now().year
        response = self.client.get(
            reverse("calendar", kwargs={"year": now_year, "month_number": now_month}), follow=True
        )
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.message, "You don't have the required permissions to access this page.")

    def test_if_owner_can_access_view(self):
        self.client.force_login(self.user_owner1)
        now_month = timezone.now().month
        now_year = timezone.now().year
        response = self.client.get(reverse("calendar", kwargs={"year": now_year, "month_number": now_month}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
