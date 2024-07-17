from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.views.generic import CreateView

from core.base import has_group, redirect_to_dashboard_based_on_group
from owner.forms import DepartmentForm


class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = DepartmentForm
    permission_required = "organizations.add_department"
    template_name = "owner/department_create.html"
    context_object_name = "department"

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        managers_ids = [
            manager.id
            for manager in User.objects.filter(profile__company=self.request.user.profile.company).all()
            if has_group(manager, "Manager")
        ]
        managers = User.objects.filter(pk__in=managers_ids)
        context["form"].fields["manager"].queryset = managers
        context["title"] = "Create Department - CloudStaffHub"
        return context

    def form_valid(self, form):
        form.instance.company = self.request.user.profile.company
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("department-list")
