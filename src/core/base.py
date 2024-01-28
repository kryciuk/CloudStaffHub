from itertools import chain

from django.http import HttpResponseRedirect
from django.urls import reverse

from .consts import GROUPS


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


def redirect_to_dashboard_based_on_group(group):
    match group:
        case GROUPS.GROUP__CANDIDATE:
            return HttpResponseRedirect(reverse("dashboard-candidate"))
        case GROUPS.GROUP__RECRUITER:
            return HttpResponseRedirect(reverse("dashboard-recruiter"))
        case GROUPS.GROUP__MANAGER:
            return HttpResponseRedirect(reverse("dashboard-manager"))
        case GROUPS.GROUP__OWNER:
            return HttpResponseRedirect(reverse("dashboard-owner"))
        case GROUPS.GROUP__EMPLOYEE:
            return HttpResponseRedirect(reverse("dashboard-employee"))
        case _:
            return HttpResponseRedirect(reverse("login"))


def make_nice_error_keys(error_dict):
    for k, v in list(error_dict.items()):
        new_key = []
        for letter in k:
            if letter.isalpha():
                new_key.append(letter)
            elif letter == "_":
                new_key.append(" ")
        new_key = "".join(new_key)
        new_key = new_key.title()
        error_dict[new_key] = error_dict.pop(k)
    return error_dict
