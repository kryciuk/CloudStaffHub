from django.test import TestCase

from organizations.factories import (
    CityFactory,
    CompanyFactory,
    DepartmentFactory,
    PositionFactory,
)
from organizations.models import City, Company, Department, Position


class TestCompanyFactories(TestCase):
    def test_company_via_factory(self):
        CompanyFactory.create()
        self.assertEqual(Company.objects.count(), 1)

    def test_company_batch_factory(self):
        CompanyFactory.create_batch(5)
        self.assertEqual(Company.objects.count(), 5)


class TestDepartmentFactory(TestCase):
    def test_department_via_factory(self):
        DepartmentFactory.create()
        self.assertEqual(Department.objects.count(), 1)

    def test_department_batch_factory(self):
        DepartmentFactory.create_batch(5)
        self.assertEqual(Department.objects.count(), 5)


class TestCityFactory(TestCase):
    def test_city_via_factory(self):
        City.objects.all().delete()
        CityFactory.create()
        self.assertEqual(City.objects.count(), 1)

    def test_city_batch_factory(self):
        City.objects.all().delete()
        CityFactory.create_batch(5)
        self.assertEqual(City.objects.count(), 5)


class TestPositionFactory(TestCase):
    def test_position_via_factory(self):
        PositionFactory.create()
        self.assertEqual(Position.objects.count(), 1)

    def test_position_batch_factory(self):
        PositionFactory.create_batch(5)
        self.assertEqual(Position.objects.count(), 5)
