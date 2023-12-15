from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import status

from recruitment.factories import JobOfferFactory, JobApplicationFactory

from recruitment.views.job_applications import (
    JobApplicationsClosedView,
    JobApplicationsDetailView,
    JobApplicationsUnderReviewView,
    JobApplicationsView,
)
from recruitment.views.job_offers import (
    JobOffersApplyView,
    JobOffersCreateView,
    JobOffersDetailView,
    JobOffersListView,
    JobOffersUpdateView,
)
from users.factories import CandidateFactory, OwnerFactory


class TestUrls(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_candidate = CandidateFactory.create()
        cls.user_owner = OwnerFactory.create()
        JobApplicationFactory.create_batch(10)

    def test_job_offers_urls_are_callable_by_name(self):
        self.client.force_login(self.user_candidate)
        response_job_offers = self.client.get(reverse("job-offers"))
        response_job_offer_detail = self.client.get(reverse("job-offer-detail", kwargs={"pk": 1}))
        response_job_offer_update = self.client.get(reverse("job-offer-update", kwargs={"pk": 2}))
        response_job_offer_apply = self.client.get(reverse("job-offer-apply", kwargs={"pk": 3}))
        self.assertEqual(response_job_offers.status_code, status.HTTP_200_OK)
        self.assertEqual(response_job_offer_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_job_offer_update.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_job_offer_apply.status_code, status.HTTP_200_OK)

    def test_job_applications_urls_are_callable_by_name(self):
        self.client.force_login(self.user_owner)
        response_job_applications = self.client.get(reverse("job-applications"))
        response_job_applications_closed = self.client.get(reverse("job-applications-closed"))
        response_job_applications_review = self.client.get(reverse("job-applications-review"))
        response_job_applications_detail = self.client.get(reverse("job-applications-detail", kwargs={"pk": 1}))
        self.assertEqual(response_job_applications.status_code, status.HTTP_200_OK)
        self.assertEqual(response_job_applications_closed.status_code, status.HTTP_200_OK)
        self.assertEqual(response_job_applications_review.status_code, status.HTTP_200_OK)
        self.assertEqual(response_job_applications_detail.status_code, status.HTTP_200_OK)



