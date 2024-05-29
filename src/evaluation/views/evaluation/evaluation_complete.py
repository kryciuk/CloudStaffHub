import json
from itertools import chain

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView

from core.base import redirect_to_dashboard_based_on_group
from evaluation.models import Evaluation


class EvaluationCompleteView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Evaluation
    context_object_name = "evaluation"
    template_name = "evaluation/evaluation/evaluation_complete.html"

    def test_func(self):
        evaluation = self.get_object()
        return self.request.user == evaluation.manager or self.request.user == evaluation.employee

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evaluation = context["object"]
        questions = evaluation.questionnaire.questions.all()
        answers = {}
        for question in questions:
            answers[question] = list(chain(question.answers.all()))
        context["answers"] = answers
        results_manager = json.loads(evaluation.result_manager)
        results_manager.pop("csrfmiddlewaretoken")
        context["results_manager_values"] = [int(element) for element in results_manager.values()]
        results_employee = json.loads(evaluation.result_employee)
        results_employee.pop("csrfmiddlewaretoken")
        context["results_employee_values"] = [int(element) for element in results_employee.values()]
        return context
