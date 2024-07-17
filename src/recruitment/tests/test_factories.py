from django.test import TestCase

from recruitment.factories import JobApplicationFactory, JobOfferFactory
from recruitment.models import JobApplication, JobOffer


class TestUserFactories(TestCase):
    def test_job_offer_via_factory(self):
        JobOfferFactory.create()
        self.assertEqual(JobOffer.objects.count(), 1)

    def test_job_offer_batch_factory(self):
        JobOfferFactory.create_batch(5)
        self.assertEqual(JobOffer.objects.count(), 5)

    def test_job_application_via_factory(self):
        JobApplicationFactory.create()
        self.assertEqual(JobApplication.objects.count(), 1)

    def test_job_application_batch_factory(self):
        JobApplicationFactory.create_batch(5)
        self.assertEqual(JobApplication.objects.count(), 5)
