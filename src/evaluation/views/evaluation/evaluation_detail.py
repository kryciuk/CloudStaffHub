from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView

from core.base import redirect_to_dashboard_based_on_group
from evaluation.forms import EvaluationCreateForm
from evaluation.models import Evaluation


class EvaluationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Evaluation
    form_class = EvaluationCreateForm
    template_name = "evaluation/evaluation/evaluation_detail.html"
    context_object_name = "evaluation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evaluation = self.get_object()
        context["title"] = f"Evaluation ID:{evaluation.id} - CloudStaffHub"
        return context

    def test_func(self):
        evaluation = self.get_object()
        return self.request.user == evaluation.manager or self.request.user == evaluation.employee

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")
