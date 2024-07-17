from django.apps import AppConfig
from django.db.models.signals import post_migrate

from core.base import _get_perms_for_models


class LandingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "landing"

    def ready(self):
        from users.signals import create_profile  # noqa: F401

        post_migrate.connect(self.populate_models, sender=self)
        post_migrate.connect(self.create_industries, sender=self)
        post_migrate.connect(self.create_departments, sender=self)

    def populate_models(self, sender, **kwargs):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType

        from evaluation.models import Evaluation, Questionnaire
        from events.models import Assignment
        from organizations.models import (
            City,
            Company,
            CompanyProfile,
            Department,
            Position,
        )
        from polls.models import Poll
        from recruitment.models import JobApplication, JobOffer
        from users.models import Profile

        # all model permissions

        models_to_fetch_owner = [JobOffer, City, Company, Position, Poll, Department, Evaluation, Questionnaire]
        models_to_fetch_manager = [JobOffer, City, Company, Position, Poll, Evaluation, Questionnaire]
        models_to_fetch_recruiter = [JobOffer, City, Position]

        # single permissions

        content_type_profile = ContentType.objects.get_for_model(Profile)
        content_type_company = ContentType.objects.get_for_model(CompanyProfile)
        content_type_job_application = ContentType.objects.get_for_model(JobApplication)
        content_type_assignment = ContentType.objects.get_for_model(Assignment)

        permission_update_profile = Permission.objects.get(
            codename="change_profile", content_type=content_type_profile
        )
        permission_update_company_profile = Permission.objects.get(
            codename="change_companyprofile", content_type=content_type_company
        )
        permission_create_job_application = Permission.objects.get(
            codename="add_jobapplication", content_type=content_type_job_application
        )
        permission_update_job_application = Permission.objects.get(
            codename="change_jobapplication", content_type=content_type_job_application
        )
        permission_view_job_application = Permission.objects.get(
            codename="view_jobapplication", content_type=content_type_job_application
        )
        permission_add_assignment = Permission.objects.get(
            codename="add_assignment", content_type=content_type_assignment
        )

        # owner

        owner, _ = Group.objects.get_or_create(name="Owner")
        owner.permissions.set(_get_perms_for_models(models_to_fetch_owner))
        owner.permissions.add(permission_update_profile)
        owner.permissions.add(permission_update_company_profile)
        owner.permissions.add(permission_update_job_application)
        owner.permissions.add(permission_view_job_application)
        owner.permissions.add(permission_add_assignment)

        # manager

        manager, _ = Group.objects.get_or_create(name="Manager")
        manager.permissions.set(_get_perms_for_models(models_to_fetch_manager))
        manager.permissions.add(permission_update_job_application)
        manager.permissions.add(permission_view_job_application)
        manager.permissions.add(permission_add_assignment)

        # recruiter

        recruiter, _ = Group.objects.get_or_create(name="Recruiter")
        recruiter.permissions.set(_get_perms_for_models(models_to_fetch_recruiter))
        recruiter.permissions.add(permission_update_job_application)
        recruiter.permissions.add(permission_view_job_application)
        recruiter.permissions.add(permission_add_assignment)

        # employee

        employee, _ = Group.objects.get_or_create(name="Employee")
        employee.permissions.add(permission_add_assignment)

        # candidate

        candidate, _ = Group.objects.get_or_create(name="Candidate")
        candidate.permissions.add(permission_create_job_application)

        # default city

        city, _ = City.objects.get_or_create(name="Warsaw", country="Poland")

    def create_industries(self, sender, **kwargs):
        from organizations.models import Industry

        for industry in Industry.IndustryChoice:
            new_industry, _ = Industry.objects.get_or_create(industry=industry)

    def create_departments(self, sender, **kwargs):
        from organizations.models import Department

        for department in Department.DepartmentChoices:
            department, _ = Department.objects.get_or_create(name=department, company=None, manager=None)
