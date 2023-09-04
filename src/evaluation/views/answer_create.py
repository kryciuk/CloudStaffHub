from django.http import Http404
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import CreateView

from evaluation.forms import AnswerForm
from evaluation.models import Answer, Question, Questionnaire


class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerForm
    context_object_name = "answer"
    template_name = "evaluation/answer_create.html"

    def form_valid(self, form):
        try:
            question = get_object_or_404(Question, pk=self.kwargs.get("id_question"))
        except Question.DoesNotExist:
            raise Http404("A question with this ID does not exist.")
        form.instance.question = question
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "answer-create",
            kwargs={
                "id_questionnaire": self.object.question.questionnaire.id,
                "id_question": self.object.question.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id_questionnaire"] = self.kwargs.get("id_questionnaire")
        return context
