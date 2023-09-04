import django_filters
from django import forms

from organizations.models import Position


class PositionFilter(django_filters.FilterSet):
    level = django_filters.MultipleChoiceFilter(
        choices=Position.Level.choices, widget=forms.CheckboxSelectMultiple
    )
    department = django_filters.MultipleChoiceFilter(
        choices=Position.Department.choices, widget=forms.CheckboxSelectMultiple
    )
    title = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains", label="Title"
    )

    class Meta:
        model = Position
        exclude = ["company"]
