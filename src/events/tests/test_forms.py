from random import choice

from django.test import TestCase
from django.utils import timezone

from events.forms import AssignmentForm, AssignmentStatusForm
from users.factories import EmployeeFactory


class TestAssignmentForm(TestCase):
    def setUp(self):
        self.employee = EmployeeFactory.create()
        self.form_data = {
            "name": "Test",
            "description": "Test description",
            "event_date": timezone.datetime.now() + timezone.timedelta(days=choice(range(30, 60))),
            "employee": [self.employee],
        }

    def test_if_form_is_valid_with_correct_data(self):
        form = AssignmentForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_form_is_invalid_with_missing_data(self):
        self.form_data.pop("name")
        form = AssignmentForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class TestAssignmentStatusForm(TestCase):
    def setUp(self):
        self.form_data = {"status": True}

    def test_if_form_is_valid_with_correct_data(self):
        form = AssignmentStatusForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_form_is_invalid_with_missing_data(self):
        self.form_data.pop("status")
        form = AssignmentForm(data=self.form_data)
        self.assertFalse(form.is_valid())
