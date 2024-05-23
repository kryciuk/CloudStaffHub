import datetime
import os

from django.test import TransactionTestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from organizations.factories import CityFactory, PositionFactory
from organizations.models import City, Department
from recruitment.factories import JobOfferFactory
from recruitment.models import JobOffer
from users.factories import CandidateFactory, EmployeeFactory, OwnerFactory


class TestJobOfferApplyView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        City.objects.all().delete()
        Department.objects.all().delete()
        self.user_candidate = CandidateFactory.create()
        self.user_owner = OwnerFactory.create()
        self.user_candidate.profile.phone_number = "+48500500500"
        self.user_candidate.profile.save()
        self.job_offer = JobOfferFactory.create(status=True)

    def test_correct_user_data_is_loaded_initially(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-apply", kwargs={"pk": self.job_offer.id}))
        self.assertEqual(response.context["form"].initial["first_name"], self.user_candidate.first_name)
        self.assertEqual(response.context["form"].initial["last_name"], self.user_candidate.last_name)
        self.assertEqual(response.context["form"].initial["email"], self.user_candidate.email)
        self.assertEqual(response.context["form"].initial["phone_number"], self.user_candidate.profile.phone_number)

    def test_candidate_cant_apply_for_non_existing_job_offer(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-apply", kwargs={"pk": 2}))
        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_only_candidate_can_access_view(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-apply", kwargs={"pk": 1}))
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("job-offer-apply", kwargs={"pk": 1}))
        self.assertTrue(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-apply", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "recruitment/job_offers/job_offer_apply.html")


class TestJobOfferCreateView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        City.objects.all().delete()
        self.user_owner = OwnerFactory.create()
        self.position = PositionFactory.create(company=self.user_owner.profile.company)
        self.user_employee = EmployeeFactory.create()
        self.city = CityFactory.create()
        self.data = {
            "position": self.position.pk,
            "description": "placeholder text",
            "country": self.city.country,
            "city": self.city.pk,
            "expiry_date": timezone.datetime(2024, 10, 12),
        }

    def test_if_job_offer_is_created_correctly(self):
        self.client.force_login(self.user_owner)
        self.client.post(reverse("job-offer-create"), data=self.data)
        self.assertEqual(JobOffer.objects.count(), 1)

    def test_if_regular_employee_cant_access_view(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("job-offer-create"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_job_offer_is_created_with_correct_data(self):
        self.client.force_login(self.user_owner)
        self.client.post(reverse("job-offer-create"), data=self.data)
        created_job_offer = JobOffer.objects.get(id=1)
        self.assertEqual(created_job_offer.position.id, self.data.get("position"))
        self.assertEqual(created_job_offer.status, True)
        self.assertEqual(created_job_offer.city.id, self.data.get("city"))
        self.assertEqual(created_job_offer.company, self.user_owner.profile.company)
        self.assertEqual(created_job_offer.published_date, timezone.datetime.today().date())
        self.assertEqual(
            created_job_offer.expiry_date, timezone.datetime(2024, 10, 12, 0, 0, tzinfo=datetime.timezone.utc)
        )

    def test_if_job_offer_is_not_created_if_missing_data(self):
        self.client.force_login(self.user_owner)
        self.data["position"] = ""
        self.client.post(reverse("job-offer-create"), data=self.data)
        self.assertEqual(JobOffer.objects.count(), 0)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("job-offer-create"))
        self.assertTemplateUsed(response, "recruitment/job_offers/job_offer_update.html")


class TestJobOfferDetailView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        City.objects.all().delete()
        self.user_candidate = CandidateFactory.create()
        self.job_offer = JobOfferFactory.create()
        self.pdf_path = "test_pdf.pdf"
        with open(self.pdf_path, "wb") as pdf:
            pdf.write(b"%PDF-1.4PDF mock file content\n")

    def tearDown(self):
        if os.path.exists(self.pdf_path):
            os.remove(self.pdf_path)

    def test_if_job_offer_is_open_if_first_applying(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-detail", kwargs={"pk": 1}))
        self.assertEqual(response.context["user_application"], False)

    def test_if_job_offer_is_not_open_if_previously_applied(self):
        self.client.force_login(self.user_candidate)
        with open(self.pdf_path, "rb") as pdf:
            self.client.post(
                reverse("job-offer-apply", kwargs={"pk": 1}),
                data={
                    "first_name": self.user_candidate.first_name,
                    "last_name": self.user_candidate.last_name,
                    "phone_number": "504400500",
                    "email": self.user_candidate.email,
                    "expected_salary": 9000,
                    "cv": pdf,
                    "consent_processing_data": True,
                },
            )
        response = self.client.get(reverse("job-offer-detail", kwargs={"pk": 1}))
        self.assertEqual(response.context["user_application"], True)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-detail", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "recruitment/job_offers/job_offer_detail.html")


class TestJobOfferListView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        City.objects.all().delete()
        Department.objects.all().delete()
        self.user_owner_1 = OwnerFactory.create()
        self.user_owner_2 = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.job_offers = JobOfferFactory.create_batch(20, company=self.user_owner_1.profile.company)
        for job_offer in self.job_offers:
            job_offer.company = self.user_owner_2.profile.company
            job_offer.save()

    def test_if_view_is_paginated_by_5(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offers"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["job_offers"]), 5)

    def test_if_owner_can_view_active_job_offers_only_assigned_to_his_company(self):
        self.client.force_login(self.user_owner_1)
        response = self.client.get(reverse("job-offers"))
        self.assertQuerySetEqual(
            response.context["object_list"],
            JobOffer.objects.filter(company=self.user_owner_1.profile.company, status=True).order_by(
                "-published_date"
            )[:5],
        )

    def test_if_candidate_can_view_all_active_job_offers(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offers"))
        self.assertQuerySetEqual(
            response.context["object_list"], JobOffer.objects.filter(status=True).order_by("-published_date")[:5]
        )

    def test_if_there_is_info_displayed_if_there_are_no_job_offers(self):
        self.client.force_login(self.user_candidate)
        JobOffer.objects.all().delete()
        response = self.client.get(reverse("job-offers"))
        self.assertContains(response, "Currently there are no job offers available...")

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offers"))
        self.assertTemplateUsed(response, "recruitment/job_offers/job_offers.html")


class TestJobOfferUpdateView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        City.objects.all().delete()
        Department.objects.all().delete()
        self.user_owner_1 = OwnerFactory.create()
        self.user_owner_2 = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_employee.profile.company = self.user_owner_1.profile.company
        self.user_employee.save()
        self.job_offer_1 = JobOfferFactory.create(company=self.user_owner_1.profile.company)
        self.job_offer_2 = JobOfferFactory.create(company=self.user_owner_2.profile.company)

    def test_if_candidate_cant_access_view(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-update", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_regular_employee_cant_access_view(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("job-offer-update", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_owner_can_access_view_for_own_company(self):
        self.client.force_login(self.user_owner_1)
        response = self.client.get(reverse("job-offer-update", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_owner_cant_access_job_offer_for_another_company(self):
        self.client.force_login(self.user_owner_1)
        response = self.client.get(reverse("job-offer-update", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner_1)
        response = self.client.get(reverse("job-offer-update", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "recruitment/job_offers/job_offer_update.html")
