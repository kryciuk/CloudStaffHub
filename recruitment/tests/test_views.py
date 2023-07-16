from django.test import Client, TestCase
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.url_candidate = reverse("candidate-default")
        self.url_job_offers = reverse("job-offers")
        self.url_job_offer_create = reverse("job-offer-create")
        self.url_job_offer_apply = reverse("job-offer-apply", args=[1])
        self.url_job_offer_detail = reverse("job-offer-detail", args=[1])
        self.test_application = {
            "first_name": "Anna",
            "last_name": "Smith",
            "phone_number": 505050,
            "email": "anna.smith@gmail.com",
            "expected_salary": 4000,
            "cv": "cv.jpg",
            "consent_processing_data": True,
        }

    def test_job_offers_GET_should_return_status_code_200(self):
        response = self.client.get(self.url_job_offers)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recruitment/job_offers.html")

    def test_job_offer_apply_post_should_return_status_code_200(self):
        response = self.client.post(self.url_job_offer_apply, self.test_application)
        print(response)
        assert 1
