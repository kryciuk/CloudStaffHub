from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import View

from recruitment.models import Company
from users.forms import CompanyForm, CreateUserForm
from users.models import Profile


class RegisterCompanyView(View):
    def post(self, request):
        form_company = CompanyForm(request.POST)
        form = CreateUserForm(request.POST)
        if not form_company.is_valid():
            context = {"form": form, "form_user": form, "title": "Register Company"}
            return render(request, "users/register_company.html", context)
        company = form_company.save()
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, company=company)
            messages.success(request, f"Company profile created for {company.name}")
            return redirect("login")

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        form_company = CompanyForm()
        form = CreateUserForm()
        context = {
            "form_company": form_company,
            "form": form,
            "title": "Register Company",
        }
        return render(request, "users/register_company.html", context)
