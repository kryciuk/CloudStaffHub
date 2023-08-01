from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from recruitment.models import Company, JobOffer


@receiver(post_save, sender=Company)
def create_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.create(name=instance.name)
        group.save()
        ct = ContentType.objects.get_for_model(model=JobOffer)
        permissions_list = Permission.objects.filter(content_type=ct)
        group.permissions.set(permissions_list)
        group.save()
