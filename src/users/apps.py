from django.apps import AppConfig
from django.db import DatabaseError
from django.db.models.signals import post_migrate

from core.base import _get_perms_for_models


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    # def ready(self):
    #     from users.signals import create_profile
    #     post_migrate.connect(self.populate_models, sender=self)
    #
    # def populate_models(self, sender, **kwargs):
    #     from django.contrib.auth.models import Group
    #
    #     from organizations.models import City, Company, Position
    #     from recruitment.models import JobApplication, JobOffer
    #
    #     models_to_fetch = [JobOffer, JobApplication, City, Company, Position]
    #
    #     creator, _ = Group.objects.get_or_create(name="Creator")
    #     perms = _get_perms_for_models(models_to_fetch)
    #     creator.permissions.set(perms)
    #
    #     recruiter, _ = Group.objects.get_or_create(name="Recruiter")
    #     recruiter.permissions.set(perms)
    #
    #     employee, _ = Group.objects.get_or_create(name="Employee")
    #
    #     candidate, _ = Group.objects.get_or_create(name="Candidate")
    #

    # def _perms_recruitment(self, models):
    #     from django.contrib.contenttypes.models import ContentType
    #     from recruitment.models import (City, Company, JobApplication, JobOffer,
    #                                     Position)
    #     from django.contrib.auth.models import Group, Permission, User
    #     # models_to_fetch = [JobOffer, City, Company, Position]
    #     try:
    #         permissions = {}
    #         for model in models:
    #             content_type = ContentType.objects.get_for_model(model=model)
    #             perms = Permission.objects.filter(content_type=content_type)
    #             permissions[model.__name__] = perms
    #         return permissions
    #     except DatabaseError as e:
    #         logger.error(f"Unexcepted DatabaseError occurs during the perms perms_recruitment {str(e)}")
    #     except Exception as e:
    #         logger.error(f"Unexcepted exception occurs during the perms perms_recruitment {str(e)}")
