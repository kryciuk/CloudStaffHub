from random import choice, randint, random

import factory
from django.contrib.auth.models import User
from factory.fuzzy import FuzzyChoice

from .choices import (
    JOB_APPLICATION_STATUS_CHOICES,
    JOB_OFFER_LEVEL_CHOICES,
    POSITION_DEPARTMENT_CHOICES,
)
from .models import City, Company, JobApplication, JobOffer, Position


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
    email_domain = factory.LazyAttribute(
        lambda z: "".join(letter for letter in z.name if letter.isalpha()) + ".com"
    )


class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position

    title = factory.Faker("job")
    level = factory.fuzzy.FuzzyChoice(JOB_OFFER_LEVEL_CHOICES, getter=lambda x: x[0])
    departament = factory.fuzzy.FuzzyChoice(
        POSITION_DEPARTMENT_CHOICES, getter=lambda x: x[0]
    )


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Faker("city")
    country = factory.Faker("country")


class JobOfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobOffer

    position = factory.SubFactory(PositionFactory)
    description = factory.Faker("sentence", nb_words=100)
    status = factory.LazyAttribute(lambda x: choice([True, False]))
    city = factory.SubFactory(CityFactory)
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
    expected_salary = factory.LazyAttribute(lambda x: randint(3000, 10000))
    cv = "cv.pdf"
    consent_processing_data = True
    status = 0


# python manage.py shell
# from recruitment.factories import PositionFactory, JobOfferFactory, UserFactory, JobApplicationFactory, CityFactory, CompanyFactory
# from recruitment.factories import UserFactory, JobApplicationFactory, CityFactory
# x = PositionFactory.create_batch(10)
# y = JobOfferFactory.create_batch(10)
# z = UserFactory.create_batch(10)
# w = JobApplicationFactory.create_batch(3)
# d = CityFactory.create_batch(3)
# a = CompanyFactory.create_batch(3)
