from django import template

register = template.Library()


@register.filter(name="has_group")
def has_group(user, group_name):
    user_groups = user.groups.values_list("name", flat=True)
    return True if group_name in user_groups else False


@register.filter("get_value_from_dict")
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)
