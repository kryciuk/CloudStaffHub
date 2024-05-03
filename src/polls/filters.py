import django_filters
from django import forms

from polls.models import Poll


class PollFilter(django_filters.FilterSet):
    questionnaire = django_filters.CharFilter(
        field_name="questionnaire__name", lookup_expr="icontains", label="Questionnaire"
    )
    date_end = django_filters.DateFilter(field_name="date_end", lookup_expr="icontains", label="Date End")
    date_created = django_filters.DateFilter(field_name="date_created", lookup_expr="icontains", label="Date Created")
    created_by = django_filters.CharFilter(
        field_name="created_by__username", lookup_expr="icontains", label="Created by"
    )
    status = django_filters.BooleanFilter(
        field_name="status", label="Show Open/Closed Polls", widget=forms.CheckboxInput(), initial=True
    )

    class Meta:
        model = Poll
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PollFilter, self).__init__(*args, **kwargs)
        self.filters["status"].field.initial = True
