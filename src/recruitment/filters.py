import django_filters
from django_filters.widgets import BooleanWidget

from recruitment.models import JobOffer
from django import forms


class JobOfferFilter(django_filters.FilterSet):
    company = django_filters.CharFilter(field_name="company__name", lookup_expr="icontains", label="Company")
    city = django_filters.CharFilter(field_name="city__name", lookup_expr="iexact", label="City")
    country = django_filters.CharFilter(field_name="city__country", lookup_expr="iexact", label="Country")
    position = django_filters.MultipleChoiceFilter(
        field_name='position__department',
        choices=JobOffer.objects.order_by('position__department').values_list('position__department', 'position__department').distinct(),
        widget=forms.CheckboxSelectMultiple,
        label="Department"
    )

    class Meta:
        model = JobOffer
        fields = ["company", "city"]
