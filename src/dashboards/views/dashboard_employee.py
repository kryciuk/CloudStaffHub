from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView


class UserHasEmployeeOrHigherGroup(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Employee').exists() or self.request.user.groups.filter(name='Manager').exists() or self.request.user.groups.filter(name='Recruiter').exists() or self.request.user.groups.filter(name='Creator').exists()


class EmployeeDashboardView(UserHasEmployeeOrHigherGroup, TemplateView):
    template_name = "dashboards/dashboard_employee.html"
