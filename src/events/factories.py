from random import choice

import factory
from django.utils import timezone
from factory.fuzzy import FuzzyChoice

from users.factories import OwnerFactory

from .models import Assignment


class AssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Assignment

    name = factory.Faker("sentence", nb_words=6)
    event_date = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=choice(range(15, 90))))
    description = factory.Faker("sentence", nb_words=20)
    manager = factory.SubFactory(OwnerFactory)
    status = FuzzyChoice([True, False])

    @factory.post_generation
    def employee(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.employee.add(*extracted)
