from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status

from organizations.models import City, Department
from recruitment.factories import JobApplicationFactory
from recruitment.models import JobApplication
from users.factories import CandidateFactory, EmployeeFactory, OwnerFactory


class TestJobOApplicationsView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        City.objects.all().delete()
        Department.objects.all().delete()
        self.user_owner = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.job_applications = JobApplicationFactory.create_batch(20)
        for job_application in self.job_applications:
            job_application.job_offer.company = self.user_owner.profile.company
            job_application.job_offer.save()
            job_application.save()

    def test_if_regular_employee_cant_access_view(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("job-applications"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_owner_can_access_view(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("job-applications"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_view_is_paginated_by_10(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("job-applications"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["job_applications"]), 10)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("job-applications"))
        self.assertTemplateUsed(response, "recruitment/job_applications/job_applications.html")


class TestJobOApplicationsClosedView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        City.objects.all().delete()
        Department.objects.all().delete()
        self.user_owner = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.job_applications = JobApplicationFactory.create_batch(20)
        for job_application in self.job_applications[:5]:
            job_application.job_offer.company = self.user_owner.profile.company
            job_application.status = 2
            job_application.job_offer.save()
            job_application.save()

    def test_if_candidate_cant_access_view(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-applications-closed"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_owner_can_access_view(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("job-applications-closed"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_owner_can_only_view_job_applications_for_own_company(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("job-applications-closed"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context["job_applications"]), 5)

    def test_if_there_is_info_displayed_if_there_are_no_job_applications(self):
        self.client.force_login(self.user_owner)
        JobApplication.objects.all().delete()
        response = self.client.get(reverse("job-applications-closed"))
        self.assertContains(response, "Currently there are no job applications...")

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("job-applications-closed"))
        self.assertTemplateUsed(response, "recruitment/job_applications/job_applications.html")


class TestJobOApplicationsUnderReviewView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        City.objects.all().delete()
        Department.objects.all().delete()
        self.user_owner = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.job_applications = JobApplicationFactory.create_batch(10)
        for job_application in self.job_applications[:5]:
            job_application.job_offer.company = self.user_owner.profile.company
            job_application.status = 1
            job_application.job_offer.save()
            job_application.save()

    def test_if_candidate_cant_access_view(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-applications-review"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_owner_can_access_view(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("job-applications-review"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_owner_can_only_view_job_applications_for_own_company(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("job-applications-review"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context["job_applications"]), 5)

    def test_if_there_is_info_displayed_if_there_are_no_job_applications(self):
        self.client.force_login(self.user_owner)
        JobApplication.objects.all().delete()
        response = self.client.get(reverse("job-applications-review"))
        self.assertContains(response, "Currently there are no job applications...")

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("job-applications-review"))
        self.assertTemplateUsed(response, "recruitment/job_applications/job_applications.html")


class TestJobOApplicationsDetailView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        City.objects.all().delete()
        Department.objects.all().delete()
        self.user_owner_1 = OwnerFactory.create()
        self.user_owner_2 = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.job_applications = JobApplicationFactory.create_batch(5)
        for job_application in self.job_applications:
            job_application.job_offer.company = self.user_owner_1.profile.company
            job_application.job_offer.save()
            job_application.save()

    def test_if_candidate_cant_access_view(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-applications-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_regular_employee_cant_access_view(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("job-applications-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_owner_cant_view_job_application_for_another_company(self):
        self.client.force_login(self.user_owner_2)
        response = self.client.get(reverse("job-applications-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_if_owner_can_change_job_application_status(self):
        self.client.force_login(self.user_owner_1)
        response = self.client.post(
            reverse("job-applications-detail", kwargs={"pk": 1}), data={"status": 2}, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(JobApplication.objects.get(pk=1).status, 2)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner_1)
        response = self.client.get(reverse("job-applications-detail", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "recruitment/job_applications/job_applications_detail.html")
