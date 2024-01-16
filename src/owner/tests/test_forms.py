from django.test import TestCase

from organizations.models import Department
from owner.forms import DepartmentForm
from users.factories import OwnerFactory


class TestDepartmentForm(TestCase):
    def setUp(self):
        self.form_data = {"name": Department.DepartmentChoices.DESIGN, "manager": OwnerFactory.create()}

    def test_if_poll_is_created_if_correct_data(self):
        form = DepartmentForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_poll_is_not_created_if_incorrect_data(self):
        self.form_data["name"] = "aa"
        form = DepartmentForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_if_poll_is_not_created_if_missing_data(self):
        self.form_data.pop("manager")
        form = DepartmentForm(data=self.form_data)
        self.assertFalse(form.is_valid())
