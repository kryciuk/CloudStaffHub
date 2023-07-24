from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

from recruitment.models import Company


@receiver(post_save, sender=Company)
def create_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.create(name=instance.name)
        group.save()
        permissions_list = Permission.objects.all()
        group.permissions.set(permissions_list)
        group.save()
