import django_filters
from django import forms

from evaluation.models import Questionnaire


class QuestionnaireFilter(django_filters.FilterSet):
    type = django_filters.MultipleChoiceFilter(choices=Questionnaire.Type.choices, widget=forms.CheckboxSelectMultiple)
    name = django_filters.CharFilter(field_name="title", lookup_expr="icontains", label="Name")
    created_by = django_filters.CharFilter(field_name="created_by", lookup_expr="icontains", label="Created by")

    class Meta:
        model = Questionnaire
        exclude = ["company", "status"]
