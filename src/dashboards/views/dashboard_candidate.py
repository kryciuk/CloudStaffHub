from random import randrange

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from organizations.models import Company
from recruitment.models import JobOffer


class CandidateDashboardView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "dashboards/dashboard_candidate.html"

    def get_context_data(self, randit=None, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.request.user.profile.interested_in
        if department:
            context["newest_entries"] = JobOffer.objects.filter(
                position__department=department.id, status=True
            ).order_by("-id")[:10]
        else:
            context["newest_entries"] = JobOffer.objects.filter(status=True).order_by("-id")[:10]
        random_company = randrange(1, len(Company.objects.all()) + 1)
        context["random_company"] = Company.objects.get(id=random_company)
        return context
