from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView

from evaluation.models import Questionnaire


class QuestionnaireDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Questionnaire
    context_object_name = "questionnaire"
    template_name = "evaluation/questionnaire_detail.html"
    permission_required = "questionnaire.view_questionnaire"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionnaire = Questionnaire.objects.get(id=self.object.id)
        questions = questionnaire.questions.all()
        answers = {}
        for question in questions:
            answers[question] = list(chain(question.answers.all()))
        context["questions"] = questions
        context["answers"] = answers
        return context
