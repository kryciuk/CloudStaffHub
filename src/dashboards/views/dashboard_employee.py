from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from evaluation.models import Evaluation


class UserHasEmployeeOrHigherGroup(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.groups.filter(name="Employee").exists()
            or self.request.user.groups.filter(name="Manager").exists()
            or self.request.user.groups.filter(name="Recruiter").exists()
            or self.request.user.groups.filter(name="Creator").exists()
        )


class EmployeeDashboardView(UserHasEmployeeOrHigherGroup, TemplateView):
    template_name = "dashboards/dashboard_employee.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assigned_evaluations = Evaluation.objects.filter(
            employee=self.request.user, status=False
        ).order_by("-date_end")[:5]
        completed_evaluations = Evaluation.objects.filter(
            employee=self.request.user, status=True
        )
        context["assigned_evaluations"] = assigned_evaluations
        context["completed_evaluations"] = completed_evaluations
        return context
