from django.forms import ModelForm, Form
from django import forms

from recruitment.models import JobApplication
from organizations.models import City, Position


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
