from django.test import TestCase

from organizations.forms import CompanyForm


class TestCompanyFormForm(TestCase):
    def setUp(self):
        self.form_data = {"name": "ABC", "email_domain": "abc.com"}

    def test_if_company_is_created_if_correct_data(self):
        form = CompanyForm(data=self.form_data)
        self.assertTrue(form.is_valid())
