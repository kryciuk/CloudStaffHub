from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.views.generic import View

from core.base import make_nice_error_keys
from organizations.forms import CompanyForm
from users.forms import CreateUserForm

# logger = logging.getLogger("CSH")


class RegisterCompanyView(View):
    def post(self, request):
        form_company = CompanyForm(request.POST)
        form = CreateUserForm(request.POST)
        if not form_company.is_valid() or not form.is_valid():
            messages.warning(request, make_nice_error_keys(form_company.errors))
            messages.warning(request, make_nice_error_keys(form.errors))
            return redirect("register-company")
        if form.is_valid() and form_company.is_valid():
            domain_user = form.clean_email().rsplit("@")[1]
            domain_company = form_company.clean_email_domain()
            if domain_user != domain_company:
                form_company.add_error("email_domain", "User and company domains do not match.")
                messages.warning(request, make_nice_error_keys(form_company.errors))
                return redirect("register-company")
            company = form_company.save()
            user = form.save()
            owner_group = Group.objects.get(name="Owner")
            owner_group.user_set.add(user)
            messages.success(request, f"Company {company.name} was registered successfully.")
            return redirect("login")

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard-employee")
        form_company = CompanyForm()
        form = CreateUserForm()
        context = {
            "form_company": form_company,
            "form": form,
            "title": "Register Company - Cloud Staff Hub",
        }
        return render(request, "organizations/register_company.html", context)
