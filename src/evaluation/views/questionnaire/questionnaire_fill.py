from itertools import chain

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView

from core.base import redirect_to_dashboard_based_on_group
from evaluation.models import Evaluation, Questionnaire


class QuestionnaireFillView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Questionnaire
    context_object_name = "questionnaire"
    template_name = "evaluation/questionnaire/questionnaire_fill.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionnaire = Questionnaire.objects.get(id=self.object.id)
        questions = questionnaire.questions.all()
        answers = {}
        for question in questions:
            answers[question] = list(chain(question.answers.all()))
        context["questions"] = questions
        context["answers"] = answers
        context["id_evaluation"] = self.kwargs.get("id_evaluation")
        evaluation = Evaluation.objects.get(id=self.kwargs.get("id_evaluation"))
        if evaluation.manager.username == self.request.user.username:
            context["is_manager"] = "yes"
        else:
            context["is_manager"] = "no"
        context["title"] = f"Evaluation Fill ID:{evaluation.id} - CloudStaffHub"
        return context

    def test_func(self):
        evaluation = Evaluation.objects.get(id=self.kwargs.get("id_evaluation"))
        return self.request.user == evaluation.manager or self.request.user == evaluation.employee

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")
