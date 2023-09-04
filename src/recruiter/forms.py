from django import forms
from django.forms import Form, ModelForm

from organizations.models import City, Position
from recruitment.models import JobApplication


class PositionsForm(ModelForm):
    class Meta:
        model = Position
        fields = ["title", "level", "department"]
        help_texts = {
            "title": None,
            "level": None,
            "departament": None,
        }


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = "__all__"
