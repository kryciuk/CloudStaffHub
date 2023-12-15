from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile

from users.factories import OwnerFactory, CandidateFactory, EmployeeFactory


class TestUserFactories(TestCase):
    def test_create_owner_via_factory(self):
        OwnerFactory.create()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_create_owner_batch_factory(self):
        OwnerFactory.create_batch(5)
        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(Profile.objects.count(), 5)

    def test_create_employee_via_factory(self):
        EmployeeFactory.create()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_create_employee_batch_factory(self):
        EmployeeFactory.create_batch(5)
        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(Profile.objects.count(), 5)

    def test_create_candidate_via_factory(self):
        CandidateFactory.create()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_create_candidate_batch_factory(self):
        CandidateFactory.create_batch(5)
        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(Profile.objects.count(), 5)