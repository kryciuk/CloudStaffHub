from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import CreateView

from core.base import redirect_to_dashboard_based_on_group
from evaluation.forms import AnswerForm
from evaluation.models import Answer, Question


class AnswerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    context_object_name = "answer"
    template_name = "evaluation/answer/answer_create.html"
    permission_required = "evaluation.add_evaluation"

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

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
