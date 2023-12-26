from django.test import tag

from django.test import TestCase

from recruiter.forms import PositionsForm, CityForm
from organizations.factories import DepartmentFactory


class TestPositionsForm(TestCase):

    def setUp(self):
        self.form_data = {
            "title": "Accountant",
            "level": "Entry",
            "department": DepartmentFactory.create()
        }

    def test_if_position_is_created_if_correct_data(self):
        form = PositionsForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_position_is_not_created_if_incorrect_data(self):
        self.form_data["level"] = 1
        form = PositionsForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_if_position_is_not_created_if_missing_data(self):
        self.form_data.pop("department")
        form = PositionsForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class TestCityForm(TestCase):

    def setUp(self):
        self.form_data = {
            "name": "Warsaw",
            "country": "Poland"
        }

    def test_if_city_is_created_if_correct_data(self):
        form = CityForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_city_is_not_created_if_incorrect_data(self):
        self.form_data["country"] = 2
        form = CityForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_if_city_is_not_created_if_missing_data(self):
        self.form_data.pop("name")
        form = CityForm(data=self.form_data)
        self.assertFalse(form.is_valid())
