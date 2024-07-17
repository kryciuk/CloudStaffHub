from random import choice, randint

import factory
from django.utils import timezone

from organizations.factories import CityFactory, CompanyFactory, PositionFactory
from users.factories import CandidateFactory

from .models import JobApplication, JobOffer


class JobOfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobOffer

    position = factory.SubFactory(PositionFactory)
    description = factory.Faker("sentence", nb_words=100)
    status = factory.LazyAttribute(lambda x: choice([True, False]))
    city = factory.SubFactory(CityFactory)
    company = factory.SubFactory(CompanyFactory)
    published_date = factory.LazyFunction(lambda: timezone.now() - timezone.timedelta(days=choice(range(1, 30))))
    expiry_date = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=choice(range(30, 60))))


class JobApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobApplication

    candidate = factory.SubFactory(CandidateFactory)
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
# from recruitment.factories import JobOfferFactory, JobApplicationFactory
# x = JobOfferFactory.create_batch(5)
# y = JobApplicationFactory.create_batch(5)
