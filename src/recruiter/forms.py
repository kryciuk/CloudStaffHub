from django.forms import ModelForm

from organizations.models import City, Position


class PositionsForm(ModelForm):
    class Meta:
        model = Position
        fields = ["title", "level", "department"]
        help_texts = {
            "title": None,
            "level": None,
            "department": None,
        }


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = "__all__"
