import django_filters
from django import forms

from organizations.models import Position


class PositionFilter(django_filters.FilterSet):
    level = django_filters.MultipleChoiceFilter(choices=Position.Level.choices, widget=forms.CheckboxSelectMultiple)
    department = django_filters.MultipleChoiceFilter(
        field_name="department__name",
        choices=Position.objects.order_by("department__name")
        .values_list("department__name", "department__name")
        .distinct(),
        widget=forms.CheckboxSelectMultiple,
        label="Department",
    )
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains", label="Title")

    class Meta:
        model = Position
        exclude = ["company"]
