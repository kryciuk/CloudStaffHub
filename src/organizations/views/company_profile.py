from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import reverse
from django.views.generic import UpdateView

from core.base import redirect_to_dashboard_based_on_group
from organizations.forms import CompanyProfileForm
from organizations.models import Company, CompanyProfile


class CompanyProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = "organizations/company_profile.html"
    model = CompanyProfile
    permission_required = "organizations.change_companyprofile"
    form_class = CompanyProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        company = Company.objects.get(id=self.object.id)
        context["title"] = f"{company.name} Profile - CloudStaffHub"
        return context

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(company=self.request.user.profile.company)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to update company profile.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_success_url(self):
        return reverse("company-profile", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        messages.success(self.request, "Company profile updated.")
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.warning(self.request, "Company profile update failed.")
        return super().form_invalid(form)
