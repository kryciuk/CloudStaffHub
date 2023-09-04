from django.urls import path

from evaluation.views import QuestionnaireCreateView, QuestionCreateView, AnswerCreateView, QuestionnaireDetailView

urlpatterns = [
    path("questionnaire/create", QuestionnaireCreateView.as_view(), name="questionnaire-create"),
    path("questionnaire/<int:id_questionnaire>/question/create", QuestionCreateView.as_view(), name="question-create"),
    path("questionnaire/<int:id_questionnaire>/question/<int:id_question>/answer/create", AnswerCreateView.as_view(), name="answer-create"),
    path("questionnaire/<int:pk>", QuestionnaireDetailView.as_view(), name="questionnaire-detail")
]
