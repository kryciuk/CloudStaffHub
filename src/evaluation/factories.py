import random
from random import choice

import factory
from django.utils import timezone
from factory import SubFactory

from evaluation.choices import ANSWERS_CHOICES
from evaluation.models import Answer, Evaluation, Question, Questionnaire
from organizations.factories import CompanyFactory
from users.factories import EmployeeFactory, OwnerFactory


class QuestionnaireFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Questionnaire

    name = factory.Faker("word")
    company = factory.SubFactory(CompanyFactory)
    created_by = factory.SubFactory(OwnerFactory)
    status = True
    type = factory.LazyAttribute(lambda x: choice([Questionnaire.Type.POLL, Questionnaire.Type.EVALUATION]))


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    text = factory.Faker("sentence", nb_words=5)
    questionnaire = factory.SubFactory(QuestionnaireFactory)


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer
        exclude = "random_number"

    random_number = factory.LazyAttribute(lambda o: _generate_random_number())
    score = factory.LazyAttribute(lambda o: ANSWERS_CHOICES[o.random_number][0])
    answer = factory.LazyAttribute(lambda o: ANSWERS_CHOICES[o.random_number][1])
    question = factory.SubFactory(QuestionFactory)


class EvaluationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Evaluation

    manager = SubFactory(OwnerFactory)
    employee = SubFactory(EmployeeFactory)
    date_created = factory.LazyFunction(lambda: timezone.now())
    date_end = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=choice(range(1, 30))))
    questionnaire = SubFactory(QuestionnaireFactory)
    result_employee = factory.Faker("boolean", chance_of_getting_true=0)
    result_manager = factory.Faker("boolean", chance_of_getting_true=0)
    status_employee = factory.Faker("boolean", chance_of_getting_true=0)
    status_manager = factory.Faker("boolean", chance_of_getting_true=0)


def _generate_random_number():
    return random.randint(0, 4)
