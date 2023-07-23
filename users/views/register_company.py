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
        if form_company.is_valid():
            form_company.save()
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                domain = form.cleaned_data.get("email").rsplit(sep="@")[-1]
                company = Company.objects.filter(email_domain=domain).first()
                user1 = User.objects.get(username=username)
                profile = Profile(user=user1, company=company)
                profile.save()
                company_name = form_company.cleaned_data.get("name")
                messages.success(request, f"Company profile created for {company_name}")
                return redirect("login")
        context = {"form": form, "form_user": form, "title": "Register Company"}
        return render(request, "users/register_company.html", context)

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
