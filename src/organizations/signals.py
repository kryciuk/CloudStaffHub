from django.db.models.signals import post_save
from django.dispatch import receiver

from organizations.models import Company, CompanyProfile


@receiver(post_save, sender=Company)
def create_company_profile(sender, instance, created, **kwargs):
    if created:
        company_profile = CompanyProfile.objects.create(company=instance)
        company_profile.save()
