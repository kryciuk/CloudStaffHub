from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from recruitment.models import JobOffer


class CandidateDashboardView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "dashboards/dashboard_candidate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.request.user.profile.interested_in
        if department:
            context["newest_entries"] = JobOffer.objects.filter(position__department=department.id).order_by("-id")[:10]
        else:
            context["newest_entries"] = JobOffer.objects.order_by("-id")[:10]
        return context
