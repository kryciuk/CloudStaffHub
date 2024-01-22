from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import reverse
from django.views.generic import UpdateView

from organizations.forms import CompanyProfileForm
from organizations.models import CompanyProfile


class CompanyProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = "organizations/company_profile.html"
    model = CompanyProfile
    permission_required = "organizations.add_companyprofile"
    form_class = CompanyProfileForm

    def get_success_url(self):
        return reverse("company-profile", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        messages.success(request, "Company profile updated.")
        return super().post(request, *args, *kwargs)
