from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import reverse
from django.views.generic import DeleteView

from organizations.models import Department


class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Department
    permission_required = "organizations.delete_department"
    context_object_name = "department"

    def get_success_url(self):
        return reverse("department-list")
