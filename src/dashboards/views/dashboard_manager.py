from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

from core.base import has_group
from evaluation.models import Evaluation
from recruitment.models import JobApplication


class UserHasManagerOrHigherGroup(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.groups.filter(name="Manager").exists()
            or self.request.user.groups.filter(name="Owner").exists()
            or self.request.user.is_superuser
        )


class ManagerDashboardView(UserHasManagerOrHigherGroup, TemplateView):
    template_name = "dashboards/dashboard_manager.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # evaluations

        assigned_evaluations = Evaluation.objects.filter(manager=self.request.user, status_manager=False).order_by(
            "-date_end"
        )[:5]
        completed_evaluations = Evaluation.objects.filter(
            manager=self.request.user, status_manager=True, status_employee=True
        ).order_by("-id")[:5]

        context["assigned_evaluations"] = assigned_evaluations
        context["evaluations_count"] = len(Evaluation.objects.filter(manager=self.request.user, status_manager=False))
        context["completed_evaluations"] = completed_evaluations

        # job applications

        review_job_applications = JobApplication.objects.filter(
            job_offer__position__department__manager=self.request.user, status=JobApplication.Status.UNDER_REVIEW
        ).order_by("-id")
        if has_group(self.request.user, "Owner"):
            review_job_applications = JobApplication.objects.filter(
                job_offer__company=self.request.user.profile.company, status=JobApplication.Status.UNDER_REVIEW
            ).order_by("-id")
        context["number_of_applications"] = len(review_job_applications)

        context["review_job_applications"] = review_job_applications

        context["title"] = "Manager's Dashboard - CloudStaffHub"

        return context
