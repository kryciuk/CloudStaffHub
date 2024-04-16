import django_filters
from django import forms

from recruitment.models import JobOffer


class JobOfferFilter(django_filters.FilterSet):
    company = django_filters.CharFilter(field_name="company__name", lookup_expr="icontains", label="Company")
    city = django_filters.CharFilter(field_name="city__name", lookup_expr="iexact", label="City")
    country = django_filters.CharFilter(field_name="city__country", lookup_expr="iexact", label="Country")
    position = django_filters.CharFilter(field_name="position__title", lookup_expr="icontains", label="Position")
    department = django_filters.MultipleChoiceFilter(
        field_name="position__department__name",
        choices=JobOffer.objects.order_by("position__department__name")
        .values_list("position__department__name", "position__department__name")
        .distinct(),
        widget=forms.CheckboxSelectMultiple,
        label="Department",
    )

    class Meta:
        model = JobOffer
        fields = ["company", "city"]
