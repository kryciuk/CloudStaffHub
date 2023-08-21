from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from recruitment.models import JobOffer


class CandidateDashboardView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "candidate/candidate_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departament = self.request.user.profile.interested_in
        context["newest_entries"] = JobOffer.objects.filter(position__departament=departament).order_by('-id')[:10]
        return context
