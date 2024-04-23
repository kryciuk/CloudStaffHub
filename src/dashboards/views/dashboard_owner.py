from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import TemplateView

from evaluation.models import Evaluation
from organizations.models import Department
from polls.models import Poll
from recruitment.models import JobApplication, JobOffer


class UserHasOwnerOrHigherGroup(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.groups.filter(name="Owner").exists() or self.request.user.is_superuser
        )


class OwnerDashboardView(UserHasOwnerOrHigherGroup, TemplateView):
    template_name = "dashboards/dashboard_owner.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.user.profile.company

        # Statistics

        context["number_of_employees"] = len(User.objects.filter(profile__company=company))
        context["number_of_departments"] = len(Department.objects.filter(company=company))

        context["number_of_open_evaluations"] = len(
            Evaluation.objects.filter(manager__profile__company=company).filter(
                Q(status_employee=False) | Q(status_manager=False)
            )
        )
        context["number_of_closed_evaluations"] = len(
            Evaluation.objects.filter(manager__profile__company=company).filter(
                Q(status_employee=True) & Q(status_manager=True)
            )
        )
        context["total_evaluations"] = context["number_of_open_evaluations"] + context["number_of_closed_evaluations"]

        context["number_of_open_polls"] = len(Poll.objects.filter(created_by__profile__company=company, status=True))
        context["number_of_closed_polls"] = len(
            Poll.objects.filter(created_by__profile__company=company, status=False)
        )
        context["total_polls"] = context["number_of_open_polls"] + context["number_of_closed_polls"]

        context["number_of_open_job_offers"] = len(JobOffer.objects.filter(company=company, status=True))
        context["number_of_closed_job_offers"] = len(JobOffer.objects.filter(company=company, status=False))
        context["total_jon_offers"] = context["number_of_open_job_offers"] + context["number_of_closed_job_offers"]

        context["number_of_pending_job_applications"] = len(
            JobApplication.objects.filter(job_offer__company=company, status=JobApplication.Status.RECEIVED)
        )
        context["total_jon_applications"] = len(JobApplication.objects.filter(job_offer__company=company))

        return context
