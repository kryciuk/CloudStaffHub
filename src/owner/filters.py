import django_filters

from organizations.models import Department


class DepartmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains", label="Department's Name")
    profile = django_filters.CharFilter(
        field_name="profile__user__username", lookup_expr="icontains", label="Employee's Username"
    )
    employee_first_name = django_filters.CharFilter(
        field_name="profile__user__first_name", lookup_expr="icontains", label="Employee's First Name"
    )
    employee_last_name = django_filters.CharFilter(
        field_name="profile__user__last_name", lookup_expr="icontains", label="Employee's Last Name"
    )

    class Meta:
        model = Department
        fields = ["name", "profile"]
