from django.test import TestCase

from evaluation.factories import (
    AnswerFactory,
    EvaluationFactory,
    QuestionFactory,
    QuestionnaireFactory,
)
from evaluation.models import Answer, Evaluation, Question, Questionnaire


class TestEvaluationFactories(TestCase):
    def test_answer_via_factory(self):
        AnswerFactory.create()
        self.assertEqual(Answer.objects.count(), 1)

    def test_answer_batch_factory(self):
        AnswerFactory.create_batch(5)
        self.assertEqual(Answer.objects.count(), 5)

    def test_question_via_factory(self):
        QuestionFactory.create()
        self.assertEqual(Question.objects.count(), 1)

    def test_question_batch_factory(self):
        QuestionFactory.create_batch(5)
        self.assertEqual(Question.objects.count(), 5)

    def test_questionnaire_via_factory(self):
        QuestionnaireFactory.create()
        self.assertEqual(Questionnaire.objects.count(), 1)

    def test_questionnaire_batch_factory(self):
        QuestionnaireFactory.create_batch(5)
        self.assertEqual(Questionnaire.objects.count(), 5)

    def test_evaluation_via_factory(self):
        EvaluationFactory.create()
        self.assertEqual(Evaluation.objects.count(), 1)

    def test_evaluation_batch_factory(self):
        EvaluationFactory.create_batch(5)
        self.assertEqual(Evaluation.objects.count(), 5)
