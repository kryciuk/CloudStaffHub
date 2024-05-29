from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import reverse
from django.views.generic import CreateView

from core.base import redirect_to_dashboard_based_on_group
from evaluation.forms import QuestionnaireForm


class QuestionnaireCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = QuestionnaireForm
    context_object_name = "questionnaire"
    template_name = "evaluation/questionnaire/questionnaire_create.html"
    permission_required = "evaluation.add_questionnaire"

    def form_valid(self, form):
        form.instance.company = self.request.user.profile.company
        form.instance.created_by = self.request.user
        form.instance.status = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("question-create", kwargs={"id_questionnaire": self.object.id})

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Questionnaire - CloudStaffHub"
        return context
