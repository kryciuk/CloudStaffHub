import factory
from factory.fuzzy import FuzzyChoice

from users.factories import OwnerFactory

from .models import City, Company, Department, Position


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
    email_domain = factory.LazyAttribute(
        lambda z: ("".join(letter for letter in z.name if letter.isalpha()) + ".com").lower()
    )


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    name = FuzzyChoice(choices=Department.DepartmentChoices.choices, getter=lambda x: x[0])
    company = factory.SubFactory(CompanyFactory)
    manager = factory.SubFactory(OwnerFactory)


class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position

    title = factory.Faker("job")
    level = factory.fuzzy.FuzzyChoice(choices=Position.Level.choices, getter=lambda x: x[0])
    department = factory.SubFactory(DepartmentFactory)
    company = factory.SubFactory(CompanyFactory)


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Faker("city")
    country = FuzzyChoice(choices=City.Country.choices, getter=lambda x: x[0])


# python manage.py shell
# from organizations.factories import CompanyFactory, DepartmentFactory, PositionFactory, CityFactory
# x = DepartmentFactory.create_batch(10)
# y = PositionFactory.create_batch(10)
# z = CityFactory.create_batch(10)
