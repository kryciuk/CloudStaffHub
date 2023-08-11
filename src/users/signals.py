from django.apps import apps
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from recruitment.apps import RecruitmentConfig
from recruitment.models import (City, Company, JobApplication, JobOffer,
                                Position)
from users.models import Profile

from .apps import UsersConfig


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        email_domain = instance.email.split(sep="@")[-1]
        print(email_domain)
        company = Company.objects.filter(email_domain=email_domain).first()
        profile = Profile.objects.create(user=instance, company=company)
        profile.save()


def populate_models(sender, **kwargs):
    from django.apps import apps
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    from .apps import UsersConfig
    creator, created = Group.objects.get_or_create(name="Creator")
    perms_job_offer, perms_job_application, perms_city, perms_company, perms_position = perms_recruitment()
    perms = perms_job_offer | perms_job_application | perms_city | perms_company | perms_position
    creator.permissions.set(perms)

    recruiter, created = Group.objects.get_or_create(name="Recruiter")
    recruiter.permissions.set(perms)

    employee, created = Group.objects.get_or_create(name="Employee")


def perms_recruitment():
    perms_job_offer = Permission.objects.filter(content_type=ContentType.objects.get_for_model(model=JobOffer))
    perms_job_application = Permission.objects.filter(
        content_type=ContentType.objects.get_for_model(model=JobApplication))
    perms_city = Permission.objects.filter(content_type=ContentType.objects.get_for_model(model=City))
    perms_company = Permission.objects.filter(content_type=ContentType.objects.get_for_model(model=Company))
    perms_position = Permission.objects.filter(content_type=ContentType.objects.get_for_model(model=Position))
    return perms_job_offer, perms_job_application, perms_city, perms_company, perms_position

# @receiver(post_save, sender=Company)
# def create_group(sender, instance, created, **kwargs):
#     if created:
#         group = Group.objects.create(name=instance.name)
#         group.save()
#         ct = ContentType.objects.get_for_model(model=JobOffer)
#         permissions_list = Permission.objects.filter(content_type=ct)
#         group.permissions.set(permissions_list)
#         group.save()
