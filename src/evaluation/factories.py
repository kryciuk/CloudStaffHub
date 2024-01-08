import random
from random import choice

import factory

from evaluation.choices import ANSWERS_CHOICES
from evaluation.models import Answer, Question, Questionnaire
from organizations.factories import CompanyFactory
from users.factories import OwnerFactory


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


def _generate_random_number():
    return random.randint(0, 4)


# python manage.py shell
# from evaluation.factories import QuestionnaireFactory, AnswerFactory
# x = QuestionnaireFactory.create()
# y = AnswerFactory.create()
