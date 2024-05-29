import json
from itertools import chain

from django.views.generic import DetailView

from evaluation.models import Evaluation


class EvaluationCompleteView(DetailView):
    model = Evaluation
    context_object_name = "evaluation"
    template_name = "evaluation/evaluation/evaluation_complete.html"

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
