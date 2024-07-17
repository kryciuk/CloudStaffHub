from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import CreateView

from core.base import redirect_to_dashboard_based_on_group
from evaluation.forms import QuestionForm
from evaluation.models import Questionnaire


class QuestionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = QuestionForm
    context_object_name = "question"
    template_name = "evaluation/question/question_create.html"
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
