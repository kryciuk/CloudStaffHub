from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

from evaluation.models import Evaluation


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
        context["assigned_evaluations"] = assigned_evaluations
        return context
