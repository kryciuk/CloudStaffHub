from django.apps import AppConfig
from django.db.models.signals import post_migrate

from core.base import _get_perms_for_models


class LandingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "landing"

    def ready(self):
        from users.signals import create_profile

        post_migrate.connect(self.populate_models, sender=self)
        post_migrate.connect(self.create_industries, sender=self)

    def populate_models(self, sender, **kwargs):
        from django.contrib.auth.models import Group

        from organizations.models import City, Company, Position
        from recruitment.models import JobApplication, JobOffer
        from polls.models import Poll

        models_to_fetch = [JobOffer, JobApplication, City, Company, Position, Poll]

        owner, _ = Group.objects.get_or_create(name="Owner")
        perms = _get_perms_for_models(models_to_fetch)
        owner.permissions.set(perms)

        recruiter, _ = Group.objects.get_or_create(name="Recruiter")
        recruiter.permissions.set(perms)

        employee, _ = Group.objects.get_or_create(name="Employee")

        candidate, _ = Group.objects.get_or_create(name="Candidate")

        manager, _ = Group.objects.get_or_create(name="Manager")

    def create_industries(self, sender, **kwargs):
        from organizations.models import Industry

        for industry in Industry.IndustryChoice:
            new_industry, _ = Industry.objects.get_or_create(industry=industry)
