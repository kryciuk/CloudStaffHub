from django.test import TestCase

from organizations.forms import CompanyForm


class TestCompanyFormForm(TestCase):
    def setUp(self):
        self.form_data = {"name": "ABC", "email_domain": "abc.com"}

    def test_if_company_is_created_if_correct_data(self):
        form = CompanyForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_company_is_not_created_if_incorrect_data(self):
        self.form_data["email_domain"] = "abc"
        form = CompanyForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_if_company_is_not_created_if_missing_data(self):
        self.form_data.pop("email_domain")
        form = CompanyForm(data=self.form_data)
        self.assertFalse(form.is_valid())
