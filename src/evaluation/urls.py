from django.urls import path

from evaluation.views import (
    AnswerCreateView,
    EvaluationCompleteView,
    EvaluationCreateView,
    EvaluationDetailView,
    EvaluationUpdateEmployeeView,
    EvaluationUpdateManagerView,
    QuestionCreateView,
    QuestionnaireCloseView,
    QuestionnaireCreateView,
    QuestionnaireDetailView,
    QuestionnaireFillView,
    QuestionnaireListByUserView,
)

urlpatterns_questionnaire = [
    path("questionnaire/create", QuestionnaireCreateView.as_view(), name="questionnaire-create"),
    path("questionnaire/<int:pk>/close", QuestionnaireCloseView.as_view(), name="questionnaire-close"),
    path("questionnaire/list", QuestionnaireListByUserView.as_view(), name="questionnaire-list"),
    path("questionnaire/<int:pk>", QuestionnaireDetailView.as_view(), name="questionnaire-detail"),
]

urlpatterns_question = [
    path("questionnaire/<int:id_questionnaire>/question/create", QuestionCreateView.as_view(), name="question-create")
]


urlpatterns_evaluation = [
    path("create", EvaluationCreateView.as_view(), name="evaluation-create"),
    path("<int:pk>/detail", EvaluationDetailView.as_view(), name="evaluation-detail"),
    path(
        "<int:id_evaluation>/detail/questionnaire/<int:pk>", QuestionnaireFillView.as_view(), name="questionnaire-fill"
    ),
    path("<int:pk>/update-manager", EvaluationUpdateManagerView.as_view(), name="evaluation-update-manager"),
    path("<int:pk>/update-employee", EvaluationUpdateEmployeeView.as_view(), name="evaluation-update-employee"),
    path("<int:pk>/complete", EvaluationCompleteView.as_view(), name="evaluation-complete"),
]

urlpatterns_answer = [
    path(
        "questionnaire/<int:id_questionnaire>/question/<int:id_question>/answer/create",
        AnswerCreateView.as_view(),
        name="answer-create",
    ),
    # path(
    #     "questionnaire/<int:id_questionnaire>/question/<int:id_question>/answer/<int:pk>/update",
    #     AnswerUpdateView.as_view(),
    #     name="answer-update",
    # ),
]

urlpatterns = []
urlpatterns += urlpatterns_questionnaire + urlpatterns_answer + urlpatterns_question + urlpatterns_evaluation
