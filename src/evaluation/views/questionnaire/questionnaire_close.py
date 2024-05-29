from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.base import redirect_to_dashboard_based_on_group
from evaluation.models import Questionnaire


class QuestionnaireCloseView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Questionnaire
    fields = ["status"]
    success_url = reverse_lazy("questionnaire-list")
    permission_required = "evaluation.update_questionnaire"
    template_name = "evaluation/questionnaire/questionnaire_detail.html"

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to perform this action.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def form_valid(self, form):
        form.instance.status = False
        return super().form_valid(form)
