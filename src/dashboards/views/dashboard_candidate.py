from random import randrange

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from organizations.consts import INDUSTRY_DEPARTMENT_MAP
from organizations.models import Company, Department, Industry
from recruitment.models import JobOffer


class CandidateDashboardView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "dashboards/dashboard_candidate.html"

    def get_context_data(self, randit=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # random company

        random_company = randrange(1, len(Company.objects.all()) + 1)
        context["random_company"] = Company.objects.get(id=random_company)

        # job offers tailored to user

        user_interested_in = self.request.user.profile.interested_in
        if not user_interested_in:
            context["newest_entries"] = JobOffer.objects.filter(status=True).order_by("-id")[:10]
        else:
            user_interested_in = self.request.user.profile.interested_in
            interests = []

            for k, v in Industry.IndustryChoice._member_map_.items():
                if v == user_interested_in.industry:
                    interests.append(v)
            key = interests[0]

            proposed_departments_for_users_industry = INDUSTRY_DEPARTMENT_MAP[key]
            active_departments = Department.objects.filter(name__in=proposed_departments_for_users_industry)
            proposed_job_offers = JobOffer.objects.filter(position__department__in=active_departments, status=True)
            context["newest_entries"] = proposed_job_offers

        return context
