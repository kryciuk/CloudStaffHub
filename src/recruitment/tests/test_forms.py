from django.utils import timezone

from django.test import TestCase

from organizations.factories import PositionFactory, CityFactory

from recruitment.forms import JobOfferForm, JobOfferFormUpdate, JobApplicationForm, JobApplicationStatusForm


class TestJobOfferForm(TestCase):

    def setUp(self):
        self.form_data = {"position": PositionFactory.create(),
                          "description": "sentence",
                          "city": CityFactory.create(),
                          "expiry_date": timezone.datetime.now()
                          }

    def test_if_job_offer_is_created_if_correct_data(self):
        form = JobOfferForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_job_offer_is_not_created_if_missing_data(self):
        self.form_data.pop("description")
        form = JobOfferForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    # def test_if_job_offer_is_not_created_if_past_date(self):
    #     self.form_data["expiry_date"] = timezone.datetime(2022, 11, 12)
    #     form = JobOfferForm(data=self.form_data)
    #     self.assertFalse(form.is_valid())


class TestJobOfferFormUpdate(TestCase):

    def setUp(self):
        self.form_data = {"position": PositionFactory.create(),
                          "description": "sentence",
                          "city": CityFactory.create(),
                          "expiry_date": timezone.datetime.now(),
                          "status": False
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
#         self.form_data = {
#                         "first_name": "John",
#                         "last_name": "Smith",
#                         "phone_number": "+48500400300",
#                         "email": "candidate1@gmail.com",
#                         "expected_salary": 9000,
#                         "cv": None,
#                         "consent_processing_data": True
#                     }

class TestJobApplicationStatusForm(TestCase):

    def test_if_job_application_is_updated_if_correct_status(self):
        form = JobApplicationStatusForm(data={"status": 1})
        self.assertTrue(form.is_valid())

    def test_if_job_application_is_not_updated_if_incorrect_status(self):
        form = JobApplicationStatusForm(data={"status": 4})
        self.assertFalse(form.is_valid())
