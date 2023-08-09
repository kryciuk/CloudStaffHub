from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from recruitment.models import Company, JobOffer, JobApplication
from users.models import Profile


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
    from .apps import UsersConfig
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    creator, created = Group.objects.get_or_create(name="creator")
    perms_job_offer = Permission.objects.filter(content_type=ContentType.objects.get_for_model(model=JobOffer))
    perms_job_application = Permission.objects.filter(content_type=ContentType.objects.get_for_model(model=JobApplication))
    perms = perms_job_offer | perms_job_application
    creator.permissions.set(perms)


# def create_creator_group_and_give_permissions():         # TODO post migrate.
#     creator, created = Group.objects.get_or_create(name="creator")
#     if created:
#         perms_job_offer = Permission.objects.filter(content_type=ContentType.objects.get_for_model(model=JobOffer))
#         perms_job_application = Permission.objects.filter(content_type=ContentType.objects.get_for_model(model=JobApplication))
#         perms = perms_job_offer | perms_job_application
#         creator.permissions.set(perms)
#     return creator
#
#





# @receiver(post_save, sender=Company)
# def create_group(sender, instance, created, **kwargs):
#     if created:
#         group = Group.objects.create(name=instance.name)
#         group.save()
#         ct = ContentType.objects.get_for_model(model=JobOffer)
#         permissions_list = Permission.objects.filter(content_type=ct)
#         group.permissions.set(permissions_list)
#         group.save()
