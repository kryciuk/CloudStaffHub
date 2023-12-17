import datetime
from unittest import mock

from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from django.test import override_settings

from freezegun import freeze_time

from users.factories import CandidateFactory, OwnerFactory
from recruitment.factories import JobOfferFactory
from organizations.factories import PositionFactory, CityFactory
from recruitment.models import JobOffer



class TestJobOfferApplyView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_candidate = CandidateFactory.create()
        self.user_owner = OwnerFactory.create()
        self.user_candidate.profile.phone_number = "+48500500500"
        self.user_candidate.profile.save()
        JobOfferFactory.create()

    def test_correct_user_data_is_loaded_initially(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-apply", kwargs={"pk": 1}))
        self.assertEqual(response.context['form'].initial['first_name'], self.user_candidate.first_name)
        self.assertEqual(response.context['form'].initial['last_name'], self.user_candidate.last_name)
        self.assertEqual(response.context['form'].initial['email'], self.user_candidate.email)
        self.assertEqual(response.context['form'].initial['phone_number'], self.user_candidate.profile.phone_number)

    def test_candidate_cant_apply_for_non_existing_job_offer(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-apply", kwargs={"pk": 2}))
        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-apply", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "recruitment/job_offers/job_offer_apply.html")


class TestJobOfferCreateView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.position = PositionFactory.create()
        self.position.company = self.user_owner.profile.company
        self.position.save()
        self.city = CityFactory.create()
        self.data = {"position": self.position.pk, "description": "placeholder text",
                     "city": self.city.pk, "expiry_date": timezone.datetime(2024, 10, 12, tzinfo=datetime.timezone.utc).date()}

    def test_if_job_offer_is_created_correctly(self):
        self.client.force_login(self.user_owner)
        self.client.post(reverse("job-offer-create"), data=self.data)
        self.assertEqual(JobOffer.objects.count(), 1)

    def test_if_job_offer_is_created_with_correct_data(self):
        self.client.force_login(self.user_owner)
        self.client.post(reverse("job-offer-create"), data=self.data)
        created_job_offer = JobOffer.objects.get(id=1)
        self.assertEqual(created_job_offer.position.id, self.data.get("position"))
        self.assertEqual(created_job_offer.status, True)
        self.assertEqual(created_job_offer.city.id, self.data.get("city"))
        self.assertEqual(created_job_offer.company, self.user_owner.profile.company)
        # self.assertEqual(created_job_offer.published_date, timezone.datetime.today().date())
        # self.assertEqual(created_job_offer.expiry_date, timezone.datetime(2024, 10, 12).date())

    def test_if_job_offer_is_not_created_if_missing_data(self):
        self.client.force_login(self.user_owner)
        self.data["position"] = ""
        self.client.post(reverse("job-offer-create"), data=self.data)
        self.assertEqual(JobOffer.objects.count(), 0)

    def test_if_message_is_displayed_after_successful_creation(self):
        self.client.force_login(self.user_owner)
        response = self.client.post(reverse("job-offer-create"), data=self.data)
        print(response.messages)


class TestJobOfferDetailView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_candidate = CandidateFactory.create()
        self.job_offer = JobOfferFactory.create()
        self.image_mock = mock.MagicMock(spec="pdf")

    def test_if_job_offer_is_open_if_first_applying(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-detail", kwargs={"pk": 1}))
        self.assertEqual(response.context["user_application"], False)

    def test_if_job_offer_is_not_open_if_previously_applied(self):
        self.client.force_login(self.user_candidate)
        self.client.post(reverse("job-offer-apply", kwargs={"pk": 1}),
                         data={"first_name": self.user_candidate.first_name,
                               "last_name": self.user_candidate.last_name,
                               "phone_number": "504400500",
                               "email": self.user_candidate.email,
                               "expected_salary": 9000,
                               "cv": self.image_mock,
                               "consent_processing_data": True})
        response = self.client.get(reverse("job-offer-detail", kwargs={"pk": 1}))
        self.assertEqual(response.context["user_application"], True)


class TestJobOfferListView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_candidate = CandidateFactory.create()
        self.job_offer = JobOfferFactory.create()
