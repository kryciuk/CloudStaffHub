from django.forms import ModelForm

from .models import Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        help_texts = {
            "position": None,
            "description": None,
            "status": None,
            "city": None,
            "published_date": None,
            "expiry_date": None,
        }

