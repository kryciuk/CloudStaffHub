import django_filters
from django import forms
from django.contrib.auth.models import User
from django_filters import OrderingFilter

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
    department = django_filters.MultipleChoiceFilter(
        field_name="profile__department__name",
        choices=User.objects.exclude(profile__department__name=None)
        .order_by("profile__department__name")
        .values_list("profile__department__name", "profile__department__name")
        .distinct(),
        widget=forms.CheckboxSelectMultiple,
        label="Department",
    )

    order_by_field = "ordering"
    ordering = OrderingFilter(
        fields=(
            ("username", "username"),
            ("first_name", "first_name"),
            ("last_name", "last_name"),
            ("email", "email"),
            ("profile__department__name", "department"),
        )
    )

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
