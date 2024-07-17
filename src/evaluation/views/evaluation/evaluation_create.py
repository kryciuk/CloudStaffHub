from datetime import datetime

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.views.generic import CreateView

from core.base import redirect_to_dashboard_based_on_group
from evaluation.forms import EvaluationCreateForm
from evaluation.models import Evaluation, Questionnaire


class EvaluationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Evaluation
    form_class = EvaluationCreateForm
    template_name = "evaluation/evaluation/evaluation_create.html"
    context_object_name = "evaluation"
    permission_required = "evaluation.add_evaluation"

    def get_context_data(self, **kwargs):
        context = super(EvaluationCreateView, self).get_context_data(**kwargs)
        available_employees = User.objects.filter(profile__company=self.request.user.profile.company)
        context["form"].fields["employee"].queryset = available_employees.exclude(id=self.request.user.id)
        context["form"].fields["questionnaire"].queryset = Questionnaire.objects.filter(
            created_by=self.request.user
        ).filter(type=Questionnaire.Type.EVALUATION)
        context["title"] = "Create Evaluation - CloudStaffHub"
        return context

    def get_form(self, form_class=EvaluationCreateForm):
        form = super().get_form()
        form.fields["date_end"].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        form.instance.manager = self.request.user
        form.instance.date_created = datetime.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dashboard-manager")

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")
