from django.forms import ModelForm

from .models import Answer, Question, Questionnaire


class QuestionnaireForm(ModelForm):
    class Meta:
        model = Questionnaire
        fields = "__all__"
        exclude = ["company"]


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        exclude = ["questionnaire"]


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = "__all__"
        exclude = ["question"]
