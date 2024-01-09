from django.test import TestCase, TransactionTestCase

from evaluation.factories import QuestionnaireFactory
from polls.factories import PollFactory
from polls.forms import PollAnswerCreateForm, PollCloseForm, PollCreateForm
from users.factories import EmployeeFactory


class TestPollCreateForm(TestCase):
    def setUp(self):
        self.form_data = {"date_end": "2030-10-10", "questionnaire": QuestionnaireFactory.create(), "status": True}

    def test_if_poll_is_created_if_correct_data(self):
        form = PollCreateForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_poll_is_not_created_if_incorrect_data(self):
        self.form_data["date_end"] = "2022-10-10"
        form = PollCreateForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_if_poll_is_not_created_if_missing_data(self):
        self.form_data.pop("questionnaire")
        form = PollCreateForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class TestPollCloseForm(TestCase):
    def test_if_poll_is_closed(self):
        form = PollCloseForm(data={})
        self.assertTrue(form.is_valid())


class TestPollAnswerCreateForm(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.employee = EmployeeFactory.create()
        questionnaire = QuestionnaireFactory.create(company=self.employee.profile.company)
        self.form_data = {
            "respondent": self.employee,
            "date_filled": "2023-10-10",
            "poll": PollFactory.create(questionnaire=questionnaire),
            "result": {},
        }

    def test_if_poll_answer_is_created_if_correct_data(self):
        form = PollAnswerCreateForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_poll_answer_is_not_created_if_missing_data(self):
        self.form_data.pop("respondent")
        form = PollAnswerCreateForm(data=self.form_data)
        self.assertFalse(form.is_valid())
