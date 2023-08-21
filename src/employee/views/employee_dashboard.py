from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView


class UserHasEmployeeGroup(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Employee').exists()


class EmployeeDashboardView(UserHasEmployeeGroup, TemplateView):
    template_name = "employee/employee_dashboard.html"
