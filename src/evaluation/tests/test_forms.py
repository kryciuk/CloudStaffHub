import random

import factory
from django.test import TestCase
from django.utils import timezone

from evaluation.factories import QuestionnaireFactory
from evaluation.forms import (
    AnswerForm,
    EvaluationCreateForm,
    QuestionForm,
    QuestionnaireForm,
)
from evaluation.models import Questionnaire
from users.factories import EmployeeFactory


class TestQuestionnaireForm(TestCase):
    def setUp(self):
        self.form_data = {"name": "Test Questionnaire", "type": Questionnaire.Type.EVALUATION}

    def test_if_questionnaire_is_created_if_correct_data(self):
        form = QuestionnaireForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_questionnaire_is_not_created_if_incorrect_data(self):
        self.form_data["type"] = "abc"
        form = QuestionnaireForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_if_questionnaire_is_not_created_if_missing_data(self):
        self.form_data.pop("name")
        form = QuestionnaireForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class TestQuestionForm(TestCase):
    def setUp(self):
        self.form_data = {"text": factory.Faker("sentence", nb_words=5)}

    def test_if_question_is_created_if_correct_data(self):
        form = QuestionForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_question_is_not_created_if_incorrect_data(self):
        self.form_data["text"] = None
        form = QuestionForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_if_question_is_not_created_if_missing_data(self):
        self.form_data.pop("text")
        form = QuestionForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class TestAnswerForm(TestCase):
    def setUp(self):
        self.form_data = {"answer": factory.Faker("word"), "score": _generate_random_number()}

    def test_if_answer_is_created_if_correct_data(self):
        form = AnswerForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_answer_is_not_created_if_incorrect_data(self):
        self.form_data["answer"] = None
        form = AnswerForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_if_answer_is_not_created_if_missing_data(self):
        self.form_data.pop("answer")
        form = AnswerForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class TestEvaluationCreateForm(TestCase):
    def setUp(self):
        self.employee = EmployeeFactory.create()
        self.date_time = timezone.now() + timezone.timedelta(days=random.choice(range(1, 30)))
        self.form_data = {
            "employee": self.employee,
            "date_end": self.date_time,
            "questionnaire": QuestionnaireFactory.create(),
        }

    def test_if_evaluation_is_created_if_correct_data(self):
        form = EvaluationCreateForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_evaluation_is_not_created_if_incorrect_data(self):
        self.form_data["date_end"] = timezone.now() - timezone.timedelta(days=random.choice(range(1, 30)))
        form = EvaluationCreateForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_if_evaluation_is_not_created_if_missing_data(self):
        self.form_data.pop("employee")
        form = AnswerForm(data=self.form_data)
        self.assertFalse(form.is_valid())


def _generate_random_number():
    return random.randint(0, 4)
