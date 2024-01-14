from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView

from organizations.models import Department
from owner.filters import DepartmentFilter


class DepartmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Department
    permission_required = "organizations.add_department"
    template_name = "owner/department_list.html"
    context_object_name = "departments"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        employees = {}
        keys = Department.objects.filter(company=self.request.user.profile.company)
        for key in keys:
            employees[key] = [
                employee
                for employee in User.objects.all()
                if employee.profile.company == self.request.user.profile.company and employee.profile.department == key
            ]
        context["employees"] = employees
        context["form"] = self.filterset.form
        return context

    def get_queryset(self):
        queryset = Department.objects.filter(company=self.request.user.profile.company)
        self.filterset = DepartmentFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
