from django.test import TestCase
from django.utils import timezone

from organizations.factories import CityFactory, PositionFactory
from recruitment.forms import JobApplicationStatusForm, JobOfferForm, JobOfferFormUpdate


class TestJobOfferForm(TestCase):
    def setUp(self):
        self.city = CityFactory.create()
        self.form_data = {
            "position": PositionFactory.create(),
            "description": "sentence",
            "country": self.city.country,
            "city": self.city.pk,
            "expiry_date": timezone.datetime.now(),
        }

    def test_if_job_offer_is_created_if_correct_data(self):
        form = JobOfferForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_job_offer_is_not_created_if_missing_data(self):
        self.form_data.pop("description")
        form = JobOfferForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_if_job_offer_is_not_created_if_past_date(self):
        self.form_data["expiry_date"] = timezone.datetime(2022, 11, 12)
        form = JobOfferForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class TestJobOfferFormUpdate(TestCase):
    def setUp(self):
        self.city = CityFactory.create()
        self.form_data = {
            "position": PositionFactory.create(),
            "description": "sentence",
            "country": self.city.country,
            "city": self.city.pk,
            "expiry_date": timezone.datetime.now(),
            "status": False,
        }

    def test_if_job_offer_is_updated_if_correct_data(self):
        form = JobOfferFormUpdate(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_job_offer_is_not_updated_if_missing_data(self):
        self.form_data.pop("description")
        form = JobOfferFormUpdate(data=self.form_data)
        self.assertFalse(form.is_valid())


# class TestJobApplicationForm(TestCase):
#
#     def setUp(self):
#         self.user_candidate = CandidateFactory.create()
#         self.pdf_path = 'test_pdf.pdf'
#         with open(self.pdf_path, 'wb') as pdf:
#             pdf.write(b'%PDF-1.4PDF mock file content\n')
#
#     def tearDown(self):
#         if os.path.exists(self.pdf_path):
#             os.remove(self.pdf_path)
#
#     @tag("x")
#     def test_if_job_application_is_submitted_if_correct_data(self):
#         with open(self.pdf_path, 'rb') as pdf:
#             form = JobApplicationForm(data={
#                 "first_name": self.user_candidate.first_name,
#                 "last_name": self.user_candidate.last_name,
#                 "phone_number": "504400500",
#                 "email": self.user_candidate.email,
#                 "expected_salary": 9000,
#                 "cv": pdf,
#                 "consent_processing_data": True})
#         self.assertTrue(form.is_valid())
#


class TestJobApplicationStatusForm(TestCase):
    def test_if_job_application_is_updated_if_correct_status(self):
        form = JobApplicationStatusForm(data={"status": 1})
        self.assertTrue(form.is_valid())

    def test_if_job_application_is_not_updated_if_incorrect_status(self):
        form = JobApplicationStatusForm(data={"status": 4})
        self.assertFalse(form.is_valid())
