from django.core.management.base import BaseCommand

from users.factories import EmployeeFactory, OwnerFactory

from ...factories import AssignmentFactory


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        manager = OwnerFactory.create()
        employees = EmployeeFactory.create_batch(5)
        print(employees)
        for employee in employees:
            employee.profile.company = manager.profile.company
            employee.profile.save()
        y = AssignmentFactory.create(employee=employees, manager=manager)
        print("queryset", y.employee.all())
