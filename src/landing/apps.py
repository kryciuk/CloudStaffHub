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
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        from organizations.models import City, Company, Position, Department, CompanyProfile
        from recruitment.models import JobApplication, JobOffer
        from polls.models import Poll
        from users.models import Profile

        models_to_fetch_owner = [JobOffer, JobApplication, City, Company, Position, Poll, Department]
        models_to_fetch_manager = [JobOffer, JobApplication, City, Company, Position, Poll]
        models_to_fetch_recruiter = [JobOffer, JobApplication, City, Position]

        owner, _ = Group.objects.get_or_create(name="Owner")
        owner.permissions.set(_get_perms_for_models(models_to_fetch_owner))
        content_type_profile = ContentType.objects.get_for_model(Profile)
        content_type_company = ContentType.objects.get_for_model(CompanyProfile)
        permission_update_profile = Permission.objects.get(codename="change_profile", content_type=content_type_profile)
        permission_update_company_profile = Permission.objects.get(codename="change_companyprofile",
                                                                   content_type=content_type_company)
        owner.permissions.add(permission_update_profile)
        owner.permissions.add(permission_update_company_profile)

        manager, _ = Group.objects.get_or_create(name="Manager")
        manager.permissions.set(_get_perms_for_models(models_to_fetch_manager))

        recruiter, _ = Group.objects.get_or_create(name="Recruiter")
        recruiter.permissions.set(_get_perms_for_models(models_to_fetch_recruiter))

        employee, _ = Group.objects.get_or_create(name="Employee")

        candidate, _ = Group.objects.get_or_create(name="Candidate")

    def create_industries(self, sender, **kwargs):
        from organizations.models import Industry

        for industry in Industry.IndustryChoice:
            new_industry, _ = Industry.objects.get_or_create(industry=industry)
