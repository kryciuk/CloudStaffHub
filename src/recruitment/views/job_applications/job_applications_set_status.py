from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.base import redirect_to_dashboard_based_on_group
from recruitment.forms import JobApplicationStatusForm
from recruitment.models import JobApplication


class JobApplicationsSetStatusUnderReviewView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = JobApplication
    permission_required = "recruitment.change_jobapplication"
    form_class = JobApplicationStatusForm
    context_object_name = "job_application"
    success_url = reverse_lazy("job-applications")

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to perform this action.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def form_valid(self, form):
        form.instance.status = 1
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Operation failed.")
        return super().form_invalid(form)


class JobApplicationsSetStatusClosedView(UpdateView):
    model = JobApplication
    permission_required = "recruitment.change_jobapplication"
    form_class = JobApplicationStatusForm
    context_object_name = "job_application"
    success_url = reverse_lazy("job-applications")

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to perform this action.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def form_valid(self, form):
        form.instance.status = 2
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Operation failed.")
        return super().form_invalid(form)


class JobApplicationsSetStatusApprovedView(UpdateView):
    model = JobApplication
    permission_required = "recruitment.change_jobapplication"
    form_class = JobApplicationStatusForm
    context_object_name = "job_application"
    success_url = reverse_lazy("job-applications")

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to perform this action.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def form_valid(self, form):
        form.instance.status = 3
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Operation failed.")
        return super().form_invalid(form)
