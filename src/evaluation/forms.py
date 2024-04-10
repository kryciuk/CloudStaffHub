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
        exclude = ["question"]


class EvaluationCreateForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = "__all__"
        exclude = ["manager", "date_created", "result_employee", "result_manager", "status_employee", "status_manager"]
        labels = {"date_end": "Deadline"}


class EvaluationUpdateEmployeeForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ["result_employee"]


class EvaluationUpdateManagerForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ["result_manager"]
