from itertools import chain

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView

from evaluation.models import Questionnaire


class QuestionnaireFillView(DetailView):
    model = Questionnaire
    context_object_name = "questionnaire"
    template_name = "evaluation/questionnaire_fill.html"

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
        return context

    def get_success_url(self):
        return redirect("evaluation-detail", args=["id_evaluation"])
