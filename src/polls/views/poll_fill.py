from itertools import chain

from django.shortcuts import redirect
from django.views.generic import DetailView
from django.shortcuts import HttpResponse

from evaluation.models import Questionnaire
from polls.models import Poll


class PollFillView(DetailView):
    model = Poll
    context_object_name = "poll"
    template_name = "polls/poll_fill.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionnaire = Questionnaire.objects.get(id=self.object.questionnaire.id)
        questions = questionnaire.questions.all()
        answers = {}
        for question in questions:
            answers[question] = list(chain(question.answers.all()))
        context["questions"] = questions
        context["answers"] = answers
        context["poll_id"] = self.object.id
        return context
