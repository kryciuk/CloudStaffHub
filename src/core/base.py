from itertools import chain


def _get_perms_for_models(models):
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    permissions = []
    for model in models:
        content_type = ContentType.objects.get_for_model(model=model)
        perms = Permission.objects.filter(content_type=content_type)
        permissions.append(perms)
    permissions_combined = list(chain(*permissions))
    return permissions_combined


def has_group(user, group):
    return user.groups.filter(name=group).exists()
