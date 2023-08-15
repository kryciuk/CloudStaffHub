from django.forms import ModelForm

from recruitment.models import City, JobApplication, Position


class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = "__all__"
        help_texts = {
            "title": None,
            "level": None,
            "departament": None,
        }


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = "__all__"
