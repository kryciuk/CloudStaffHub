import json
from itertools import chain

from django.views.generic import DetailView

from evaluation.models import Evaluation


class EvaluationCompleteView(DetailView):
    model = Evaluation
    context_object_name = "evaluation"
    template_name = "evaluation/evaluation_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evaluation = context["object"]
        questions = evaluation.questionnaire.questions.all()
        answers = {}
        for question in questions:
            answers[question] = list(chain(question.answers.all()))
        context["answers"] = answers
        results = json.loads(evaluation.result)
        results.pop("csrfmiddlewaretoken")
        context["results_values"] = [int(element) for element in results.values()]
        return context
