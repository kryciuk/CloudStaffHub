from random import choice

import factory
from django.utils import timezone

from evaluation.factories import QuestionnaireFactory
from evaluation.models import Questionnaire
from polls.models import Poll
from users.factories import OwnerFactory


class PollFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Poll

    date_end = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=choice(range(1, 30))))
    date_created = factory.LazyFunction(lambda: timezone.now())
    created_by = factory.SubFactory(OwnerFactory)
    questionnaire = factory.SubFactory(QuestionnaireFactory, type=Questionnaire.Type.POLL)
    status = True


# python manage.py shell
# from polls.factories import PollFactory
# x = PollFactory.create()
