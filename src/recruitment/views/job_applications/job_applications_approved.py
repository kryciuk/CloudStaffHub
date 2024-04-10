from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView

from core.base import redirect_to_dashboard_based_on_group
from recruitment.models import JobApplication


class JobApplicationsApprovedView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = JobApplication
    permission_required = "recruitment.view_jobapplication"
    template_name = "recruitment/job_applications/job_applications.html"
    context_object_name = "job_applications"
    queryset = JobApplication.objects.filter(status=JobApplication.Status.APPROVED).order_by("-id")
    paginate_by = 10

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_queryset(self):
        return JobApplication.objects.filter(
            job_offer__company=self.request.user.profile.company, status=JobApplication.Status.APPROVED
        ).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Job Applications Approved - CloudStaffHub"
        return context
