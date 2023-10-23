from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView


class UserHasRecruiterOrHigherGroup(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (
                self.request.user.groups.filter(name="Recruiter").exists()
                or self.request.user.groups.filter(name="Manager").exists()
                or self.request.user.groups.filter(name="Owner").exists()
                or self.request.user.is_superuser
        )


class RecruiterDashboardView(TemplateView):  # PermissionRequiredMixin,
    template_name = "dashboards/dashboard_recruiter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Recruiter"
        return context
