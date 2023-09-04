from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from recruitment.models import Company
from users.models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        email_domain = instance.email.split(sep="@")[-1]
        company = Company.objects.filter(email_domain=email_domain).first()
        profile = Profile.objects.create(user=instance, company=company)
        profile.save()
