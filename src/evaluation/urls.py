from django.urls import path

from evaluation.views.evaluation_dashboard import EvaluationDashboard
from evaluation.views.question_create import QuestionCreate

urlpatterns = [
    path("", EvaluationDashboard.as_view(), name="evaluation-dashboard"),
    path("question", QuestionCreate.as_view(), name='question-create')
        ]