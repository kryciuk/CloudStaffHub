from django.test import TestCase

from events.factories import AssignmentFactory
from events.models import Assignment
from users.factories import EmployeeFactory, OwnerFactory


class TestAssignmentFactories(TestCase):
    def test_assignment_via_factory(self):
        manager = OwnerFactory.create()
        employees = EmployeeFactory.create_batch(5)
        for employee in employees:
            employee.profile.company = manager.profile.company
            employee.profile.save()
        AssignmentFactory.create(employee=employees, manager=manager)
        self.assertEqual(Assignment.objects.count(), 1)

    def test_assignment_batch_factory(self):
        AssignmentFactory.create_batch(5)
        self.assertEqual(Assignment.objects.count(), 5)
