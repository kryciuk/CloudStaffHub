import pytz
from django import forms
from django.forms import ModelForm
from django.utils import timezone

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
        labels = {"text": "Question Text"}


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = "__all__"
        exclude = ["question"]
        labels = {"answer": "Answer Text"}


class EvaluationCreateForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = "__all__"
        exclude = ["manager", "date_created", "result_employee", "result_manager", "status_employee", "status_manager"]
        labels = {"date_end": "Deadline"}
        error_messages = {"date_end_future": "The end date must be in the future."}

    def clean_date_end(self):
        date_end = self.cleaned_data["date_end"]
        tz = pytz.timezone("UTC")
        today = timezone.datetime.today()
        today = today.astimezone(tz)
        if date_end < today:
            raise forms.ValidationError(self.Meta.error_messages["date_end_future"], code="date_end_future")
        return date_end


class EvaluationUpdateEmployeeForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ["result_employee"]


class EvaluationUpdateManagerForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ["result_manager"]
