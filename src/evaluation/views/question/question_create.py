from django.http import Http404
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import CreateView

from evaluation.forms import QuestionForm
from evaluation.models import Questionnaire


class QuestionCreateView(CreateView):
    form_class = QuestionForm
    context_object_name = "question"
    template_name = "evaluation/question/question_create.html"

    def form_valid(self, form):
        try:
            obj = get_object_or_404(Questionnaire, pk=self.kwargs.get("id_questionnaire"))
        except Questionnaire.DoesNotExist:
            raise Http404("A job offer with this ID does not exist.")
        form.instance.questionnaire = obj
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "answer-create",
            kwargs={
                "id_questionnaire": self.object.questionnaire.id,
                "id_question": self.object.id,
            },
        )
