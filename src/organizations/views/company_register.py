import logging

from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.views.generic import View

from organizations.forms import CompanyForm
from users.forms import CreateUserForm

logger = logging.getLogger("CSH")


class RegisterCompanyView(View):
    def post(self, request):
        form_company = CompanyForm(request.POST)
        form = CreateUserForm(request.POST)
        if not form_company.is_valid():
            logger.info(f"Failed to validate form_company form:  {form_company.errors}")
            context = {"form": form, "form_user": form, "title": "Register Company"}
            return render(request, "organizations/register_company.html", context)
        company = form_company.save()
        if form.is_valid():
            user = form.save()
            owner_group = Group.objects.get(name="Owner")
            owner_group.user_set.add(user)
            messages.success(request, f"Company profile created for {company.name}")
            return redirect("login")

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard-employee")
        form_company = CompanyForm()
        form = CreateUserForm()
        context = {
            "form_company": form_company,
            "form": form,
            "title": "Register Company",
        }
        return render(request, "organizations/register_company.html", context)
