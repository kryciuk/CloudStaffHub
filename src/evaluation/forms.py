from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Answer, Evaluation, Question, Questionnaire


class QuestionnaireForm(ModelForm):
    class Meta:
        model = Questionnaire
        fields = "__all__"
        exclude = ["company", "created_by", "status"]


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        exclude = ["questionnaire", "selected_answer"]


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = "__all__"
        exclude = ["question", "picked"]


class AnswerPickedForm(ModelForm):
    class Meta:
        model = Answer
        fields = ["picked"]


class EvaluationCreateForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = "__all__"
        exclude = ["manager", "date_created", "result", "status"]
        labels = {"date_end": "Deadline"}


class EvaluationUpdateForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ["result"]
