from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView

from core.base import redirect_to_dashboard_based_on_group
from owner.filters import EmployeeFilter


class EmployeesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "owner/employees_list.html"
    context_object_name = "employees"
    queryset = User.objects.all()
    permission_required = "organizations.add_department"

    def get_queryset(self):
        queryset = User.objects.filter(profile__company=self.request.user.profile.company).all()
        self.filterset = EmployeeFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filterset.form
        context["title"] = "Employees - CloudStaffHub"
        context["company"] = self.request.user.profile.company.name

        return context

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to view list of employees.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_success_url(self):
        return reverse("employees_list")
