from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status

from recruitment.factories import JobApplicationFactory, JobOfferFactory
from users.factories import CandidateFactory, OwnerFactory


class TestUrls(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_candidate = CandidateFactory.create()
        self.user_owner = OwnerFactory.create()
        job_offer = JobOfferFactory.create(company=self.user_owner.profile.company)
        job_offer.save()
        JobApplicationFactory.create_batch(10, job_offer=job_offer)

    def test_job_offers_urls_are_callable_by_name_for_owner(self):
        self.client.force_login(self.user_owner)
        urls_ok = {
            "job-offers": reverse("job-offers"),
            "job-offer-detail": reverse("job-offer-detail", kwargs={"pk": 1}),
            "job-offer-update": reverse("job-offer-update", kwargs={"pk": 1}),
        }
        urls_forbidden = {
            "job-offer-apply": reverse("job-offer-apply", kwargs={"pk": 1}),
        }

        for name, url in urls_ok.items():
            with self.subTest(url_name=name):
                res = self.client.get(url)
                self.assertEqual(res.status_code, status.HTTP_200_OK)
        for name, url in urls_forbidden.items():
            with self.subTest(url_name=name):
                res = self.client.get(url)
                self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_applications_urls_are_callable_by_name_for_owner(self):
        self.client.force_login(self.user_owner)
        urls = {
            "job-applications": reverse("job-applications"),
            "job-applications-closed": reverse("job-applications-closed"),
            "job-applications-review": reverse("job-applications-review"),
            "job-applications-detail": reverse("job-applications-detail", kwargs={"pk": 1}),
        }

        for name, url in urls.items():
            with self.subTest(url_name=name):
                res = self.client.get(url)
                self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_job_applications_urls_are_callable_by_name_for_candidate(self):
        self.client.force_login(self.user_candidate)
        urls = {
            "job-applications": reverse("job-applications"),
            "job-applications-closed": reverse("job-applications-closed"),
            "job-applications-review": reverse("job-applications-review"),
            "job-applications-detail": reverse("job-applications-detail", kwargs={"pk": 1}),
        }

        for name, url in urls.items():
            with self.subTest(url_name=name):
                res = self.client.get(url)
                self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
