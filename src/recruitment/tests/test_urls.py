from django.test import TestCase
from django.urls import resolve, reverse

from recruitment.views.candidate_default import CandidateDefaultView
from recruitment.views.job_offers.job_offers_list import JobOffersView


class TestUrls(TestCase):
    def setUp(self):
        self.url_candidate = reverse("candidate-default")
        self.url_job_offers = reverse("job-offers")
        self.url_job_offer_create = reverse("job-offer-create")

    def test_candidate_url_is_resolved(self):
        assert resolve(self.url_candidate).func.view_class == CandidateDefaultView

    def test_job_offers_url_is_resolved(self):
        assert resolve(self.url_job_offers).func.view_class == JobOffersView
