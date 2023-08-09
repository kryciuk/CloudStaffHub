from django.contrib import messages
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render
from django.views.generic import View

from recruitment.models import Company, JobApplication, JobOffer
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
            # creator_group = create_creator_group_and_give_permissions()
            creator_group = Group.objects.get(name="creator")
            creator_group.user_set.add(user)
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


# def create_creator_group_and_give_permissions():         # TODO post migrate.
#     creator, created = Group.objects.get_or_create(name="creator")
#     if created:
#         perms_job_offer = Permission.objects.filter(content_type=ContentType.objects.get_for_model(model=JobOffer))
#         perms_job_application = Permission.objects.filter(content_type=ContentType.objects.get_for_model(model=JobApplication))
#         perms = perms_job_offer | perms_job_application
#         creator.permissions.set(perms)
#     return creator
