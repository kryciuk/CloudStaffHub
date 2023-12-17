import datetime

from django.test import tag
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone

from users.factories import CandidateFactory, OwnerFactory
from recruitment.factories import JobOfferFactory
from organizations.factories import PositionFactory, CityFactory
from recruitment.models import JobOffer


# def create_users_and_objects_for_tests():
#     user_owner_1 = OwnerFactory.create()
#     user_owner_2 = OwnerFactory.create()
#     user_candidate = CandidateFactory.create()
#     job_offers_for_owner_1 = JobOfferFactory.create_batch(10)
#     job_offers_for_owner_2 = JobOfferFactory.create_batch(15)

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
        self.user_owner = OwnerFactory.create()
        self.position = PositionFactory.create()
        self.position.company = self.user_owner.profile.company
        self.position.save()
        self.city = CityFactory.create()
        self.data = {"position": self.position.pk, "description": "placeholder text",
                     "city": self.city.pk,
                     "expiry_date": timezone.datetime(2024, 10, 12, tzinfo=datetime.timezone.utc).date()}

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

    # do poprawy
    # def test_if_message_is_displayed_after_successful_creation(self):
    #     self.client.force_login(self.user_owner)
    #     response = self.client.post(reverse("job-offer-create"), data=self.data)
    #     message = list(response.context.get("messages"))[0]

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("job-offer-create"))
        self.assertTemplateUsed(response, "recruitment/job_offers/job_offer_update.html")


class TestJobOfferDetailView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_candidate = CandidateFactory.create()
        self.job_offer = JobOfferFactory.create()
        # self.image_mock = mock.MagicMock(spec="pdf")

    def test_if_job_offer_is_open_if_first_applying(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-detail", kwargs={"pk": 1}))
        self.assertEqual(response.context["user_application"], False)

    # do poprawy
    # def test_if_job_offer_is_not_open_if_previously_applied(self):
    #     self.client.force_login(self.user_candidate)
    #     self.client.post(reverse("job-offer-apply", kwargs={"pk": 1}),
    #                      data={"first_name": self.user_candidate.first_name,
    #                            "last_name": self.user_candidate.last_name,
    #                            "phone_number": "504400500",
    #                            "email": self.user_candidate.email,
    #                            "expected_salary": 9000,
    #                            # "cv": self.image_mock,
    #                            "consent_processing_data": True})
    #     response = self.client.get(reverse("job-offer-detail", kwargs={"pk": 1}))
    #     self.assertEqual(response.context["user_application"], True)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-detail", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "recruitment/job_offers/job_offer_detail.html")


class TestJobOfferListView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner_1 = OwnerFactory.create()
        self.user_owner_2 = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.job_offers_for_owner_1 = JobOfferFactory.create_batch(10)
        self.job_offers_for_owner_2 = JobOfferFactory.create_batch(15)
        for job_offer in self.job_offers_for_owner_1:
            job_offer.company = self.user_owner_1.profile.company
            job_offer.save()
        for job_offer in self.job_offers_for_owner_2:
            job_offer.company = self.user_owner_2.profile.company
            job_offer.save()

    def test_if_view_is_paginated_by_5(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offers"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('is_paginated' in response.context)
        self.assertLessEqual(len(response.context['object_list']), 5)

    def test_if_owner_can_view_active_job_offers_only_assigned_to_his_company(self):
        self.client.force_login(self.user_owner_1)
        response = self.client.get(reverse("job-offers"))
        self.assertQuerysetEqual(response.context['object_list'],
                                 JobOffer.objects.filter(company=self.user_owner_1.profile.company,
                                                         status=True).order_by("-published_date")[:5])

    def test_if_candidate_can_view_all_active_job_offers(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offers"))
        self.assertQuerysetEqual(response.context['object_list'],
                                 JobOffer.objects.filter(status=True).order_by("-published_date")[:5])

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
        self.user_owner_1 = OwnerFactory.create()
        self.user_owner_2 = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.job_offer_1 = JobOfferFactory.create()
        self.job_offer_2 = JobOfferFactory.create()
        self.job_offer_1.company = self.user_owner_1.profile.company
        self.job_offer_1.save()
        self.job_offer_2.company = self.user_owner_2.profile.company
        self.job_offer_2.save()

    def test_if_candidate_cant_access_view(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("job-offer-update", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_owner_can_access_view_for_own_company(self):
        self.client.force_login(self.user_owner_1)
        response = self.client.get(reverse("job-offer-update", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_owner_cant_access_job_offer_for_another_company(self):
        self.client.force_login(self.user_owner_1)
        response = self.client.get(reverse("job-offer-update", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner_1)
        response = self.client.get(reverse("job-offer-update", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "recruitment/job_offers/job_offer_update.html")
