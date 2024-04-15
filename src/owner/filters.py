import django_filters
from django.contrib.auth.models import User

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


class EmployeeFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name="username", lookup_expr="icontains", label="Username")
    first_name = django_filters.CharFilter(field_name="first_name", lookup_expr="icontains", label="First Name")
    last_name = django_filters.CharFilter(field_name="last_name", lookup_expr="icontains", label="Last Name")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains", label="Email")

    class Meta:
        model = User
        exclude = [
            "password",
            "last_login",
            "user_permissions",
            "is_staff",
            "is_active",
            "is_superuser",
            "date_joined",
            "groups",
        ]
        labels = {"first_name": "First Name"}
