from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

from core.base import redirect_to_dashboard_based_on_group
from recruitment.models import JobApplication, JobOffer


class RecruiterDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboards/dashboard_recruiter.html"

    def test_func(self):
        groups = ["Recruiter", "Manager", "Owner"]
        return (
            self.request.user.is_authenticated
            and (self.request.user.groups.filter(name__in=groups).exists())
            or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Recruiter's Dashboard - CloudStaffHub"

        # ongoing recruitment

        recruitment_info = {}
        recruitment = JobApplication.objects.filter(
            job_offer__company=self.request.user.profile.company, status=0
        ).order_by("-id")
        context["number_of_applications"] = len(recruitment)
        recruitment = recruitment[:5]
        for job_application in recruitment:
            recruitment_info.setdefault(job_application.job_offer, []).append(job_application)

        context["recruitment_info"] = recruitment_info

        # statistics job offers

        company_job_offers_all = len(JobOffer.objects.filter(company=self.request.user.profile.company))
        if len(JobOffer.objects.all()) == 0:
            company_job_offers_percentage = 0
        else:
            company_job_offers_percentage = (
                len(JobOffer.objects.filter(company=self.request.user.profile.company)) / len(JobOffer.objects.all())
            ) * 100

        context["company_job_offers_all"] = company_job_offers_all
        context["company_job_offers_percentage"] = company_job_offers_percentage

        # statistics job applications

        company_job_applications = len(
            JobApplication.objects.filter(job_offer__company=self.request.user.profile.company)
        )
        company_job_applications_received = len(
            JobApplication.objects.filter(
                job_offer__company=self.request.user.profile.company, status=JobApplication.Status.RECEIVED
            )
        )
        company_job_applications_under_review = len(
            JobApplication.objects.filter(
                job_offer__company=self.request.user.profile.company, status=JobApplication.Status.UNDER_REVIEW
            )
        )
        company_job_applications_closed = len(
            JobApplication.objects.filter(
                job_offer__company=self.request.user.profile.company, status=JobApplication.Status.CLOSED
            )
        )
        company_job_applications_approved = len(
            JobApplication.objects.filter(
                job_offer__company=self.request.user.profile.company, status=JobApplication.Status.APPROVED
            )
        )

        context["company_job_applications"] = company_job_applications
        context["company_job_applications_received"] = company_job_applications_received
        context["company_job_applications_under_review"] = company_job_applications_under_review
        context["company_job_applications_closed"] = company_job_applications_closed
        context["company_job_applications_approved"] = company_job_applications_approved

        # title

        context["title"] = "Recruiter's Dashboard - CloudStaffHub"

        return context
