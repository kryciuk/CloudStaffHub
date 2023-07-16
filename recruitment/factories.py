from random import choice, randint, random

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
from .models import JobApplication, JobOffer, Position


class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position

    title = factory.Faker("job")
    level = factory.fuzzy.FuzzyChoice(JOB_OFFER_LEVEL_CHOICES, getter=lambda x: x[0])
    departament = factory.fuzzy.FuzzyChoice(
        POSITION_DEPARTMENT_CHOICES, getter=lambda x: x[0]
    )


class JobOfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobOffer

    position = factory.SubFactory(PositionFactory)
    description = factory.Faker("sentence", nb_words=100)
    status = choice([True, False])
    city = factory.fuzzy.FuzzyChoice(JOB_OFFER_CITIES_CHOICES, getter=lambda x: x[0])
    published_date = factory.Faker("date")
    expiry_date = factory.Faker("date")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda x: f"{x.first_name}.{x.last_name}@gmail.com")
    password = factory.PostGenerationMethodCall("set_password", "P@ss1")


class JobApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobApplication

    candidate = factory.SubFactory(UserFactory)
    job_offer = factory.SubFactory(JobOfferFactory)
    first_name = factory.SelfAttribute("candidate.first_name")
    last_name = factory.SelfAttribute("candidate.last_name")
    phone_number = factory.Faker("msisdn")
    email = factory.SelfAttribute("candidate.email")
    expected_salary = randint(3000, 10000)
    cv = "cv.pdf"
    consent_processing_data = True
    status = 1


# python manage.py shell
# from recruitment.factories import PositionFactory, JobOfferFactory, UserFactory, JobApplicationFactory
# from recruitment.factories import UserFactory, JobApplicationFactory
# x = PositionFactory.create_batch(10)
# y = JobOfferFactory.create_batch(10)
# z = UserFactory.create_batch(10)
# w = JobApplicationFactory.create_batch(3)
