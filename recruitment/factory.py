import factory
from django.contrib.auth.models import User
from factory.faker import faker
from factory.fuzzy import FuzzyChoice

from .choices import (
    JOB_APPLICATION_STATUS_CHOICES,
    JOB_OFFER_CITIES_CHOICES,
    JOB_OFFER_LEVEL_CHOICES,
    POSITION_DEPARTMENT_CHOICES,
)
from .models import Position


class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position

    title = factory.Faker("job")
    level = factory.fuzzy.FuzzyChoice(JOB_OFFER_LEVEL_CHOICES, getter=lambda x: x[0])
    departament = factory.fuzzy.FuzzyChoice(
        POSITION_DEPARTMENT_CHOICES, getter=lambda x: x[0]
    )
