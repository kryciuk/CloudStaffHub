import factory
from django.contrib.auth.models import Group, User

from organizations.models import Company


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
    email_domain = factory.LazyAttribute(
        lambda z: ("".join(letter for letter in z.name if letter.isalpha()) + ".com").lower()
    )


class OwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        exclude = ["sub_object"]

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    sub_object = factory.SubFactory(CompanyFactory)
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@{obj.sub_object.email_domain}")
    plaintext_password = factory.PostGenerationMethodCall("set_password", "password")

    @factory.post_generation
    def set_owner_status(self, create, extracted, **kwargs):
        if not create:
            return
        owner_group = Group.objects.get(name="Owner")
        owner_group.user_set.add(self)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        instance.save()


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        exclude = ["sub_object"]

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    sub_object = factory.SubFactory(CompanyFactory)
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@{obj.sub_object.email_domain}")
    plaintext_password = factory.PostGenerationMethodCall("set_password", "password")

    @factory.post_generation
    def set_employee_status(self, create, extracted, **kwargs):
        if not create:
            return
        employee_group = Group.objects.get(name="Employee")
        employee_group.user_set.add(self)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        instance.save()


class CandidateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    plaintext_password = factory.PostGenerationMethodCall("set_password", "password")

    @factory.post_generation
    def set_candidate_status(self, create, extracted, **kwargs):
        if not create:
            return
        candidate_group = Group.objects.get(name="Candidate")
        candidate_group.user_set.add(self)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        instance.save()


# # python manage.py shell
# # from users.factory import EmployeeFactory, OwnerFactory
# # from organizations.factory import CompanyFactory
# # x = UserFactory.create_batch(10)
# # y = OwnerFactory.create_batch(10)
