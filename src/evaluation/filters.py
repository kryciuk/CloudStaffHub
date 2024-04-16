import django_filters
from django import forms

from evaluation.models import Questionnaire


class QuestionnaireFilter(django_filters.FilterSet):
    type = django_filters.MultipleChoiceFilter(choices=Questionnaire.Type.choices, widget=forms.CheckboxSelectMultiple)
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains", label="Title")
    created_by = django_filters.CharFilter(
        field_name="created_by__username", lookup_expr="icontains", label="Created by"
    )

    class Meta:
        model = Questionnaire
        exclude = ["company", "status"]
