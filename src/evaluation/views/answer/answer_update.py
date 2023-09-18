from django.shortcuts import get_object_or_404, reverse
from django.views.generic import UpdateView

from evaluation.forms import AnswerPickedForm
from evaluation.models import Answer, Question, Questionnaire


class AnswerUpdateView(UpdateView):
    model = Answer
    form_class = AnswerPickedForm
    template_name = "evaluation/answer_update.html"
    context_object_name = "answer"

    def get_success_url(self):
        return reverse(
            "questionnaire-detail", kwargs={"pk": self.kwargs.get("id_questionnaire")}
        )
