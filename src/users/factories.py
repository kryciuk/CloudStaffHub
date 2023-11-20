import factory
from django.contrib.auth.models import User, Group

from organizations.factory import CompanyFactory

# class UserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = User
#         abstract = True
#         exclude = ['sub_object']
#
#     username = factory.Faker("user_name")
#     first_name = factory.Faker("first_name")
#     last_name = factory.Faker("last_name")
#     sub_object = factory.SubFactory(CompanyFactory)
#     # email = factory.LazyAttribute(lambda obj: f'{obj.username}@{obj.sub_object.email_domain}')
#     plaintext_password = factory.PostGenerationMethodCall('set_password', 'password')
#
#
#     @factory.lazy_attribute
#     def email(self):
#         if hasattr(self, 'sub_object'):
#             f'{self.username}@{self.sub_object.email_domain}'
#         return f'{self.username}@example.com'
#
#     @classmethod
#     def _create(cls, model_class, *args, **kwargs):
#         user = super()._create(model_class, *args, **kwargs)
#         if hasattr(cls, 'set_status'):
#             cls.set_status(user)
#         return user
#
# class OwnerFactory(UserFactory):
#     @staticmethod
#     def set_status(user):
#         owner_group = Group.objects.get(name="Owner")
#         owner_group.user_set.add(user)
#
#     @factory.post_generation
#     def sub_object(self, create, extracted, **kwargs):
#         if not create:
#             return
#         return CompanyFactory()
#
# class EmployeeFactory(UserFactory):
#     @staticmethod
#     def set_status(user):
#         owner_group = Group.objects.get(name="Employee")
#         owner_group.user_set.add(user)
#
#     @factory.post_generation
#     def sub_object(self, create, extracted, **kwargs):
#         if not create:
#             return
#         return CompanyFactory()
#
# class CandidateFactory(UserFactory):
#     @staticmethod
#     def set_status(user):
#         owner_group = Group.objects.get(name="Candidate")
#         owner_group.user_set.add(user)


class OwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        exclude = ['sub_object']

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    sub_object = factory.SubFactory(CompanyFactory)
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@{obj.sub_object.email_domain}')
    plaintext_password = factory.PostGenerationMethodCall('set_password', 'password')

    @factory.post_generation
    def set_owner_status(self, create, extracted, **kwargs):
        if not create:
            return
        owner_group = Group.objects.get(name="Owner")
        owner_group.user_set.add(self)


class EmployeeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        exclude = ['sub_object']

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    sub_object = factory.SubFactory(CompanyFactory)
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@{obj.sub_object.email_domain}')
    plaintext_password = factory.PostGenerationMethodCall('set_password', 'password')

    @factory.post_generation
    def set_employee_status(self, create, extracted, **kwargs):
        if not create:
            return
        owner_group = Group.objects.get(name="Employee")
        owner_group.user_set.add(self)


class CandidateFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    plaintext_password = factory.PostGenerationMethodCall('set_password', 'password')

    @factory.post_generation
    def set_candidate_status(self, create, extracted, **kwargs):
        if not create:
            return
        owner_group = Group.objects.get(name="Candidate")
        owner_group.user_set.add(self)


# # python manage.py shell
# # from users.factory import EmployeeFactory, OwnerFactory
# # from organizations.factory import CompanyFactory
# # x = UserFactory.create_batch(10)
# # y = OwnerFactory.create_batch(10)
