from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.views.generic import View

from recruitment.models import Company
from users.forms import CreateUserForm
from users.models import Profile


class RegisterView(View):
    def post(self, request):
        form = CreateUserForm(request.POST)
        if not form.is_valid():
            return render(
                request, "users/authorization/register.html", {"form": form, "title": "Register"}
            )

        user = form.save()
        username = user.username
        email_domain = user.email.split(sep="@")[-1]
        company = Company.objects.filter(email_domain=email_domain).first()
        if company is None:
            candidate_group = Group.objects.get(name="Candidate")
            candidate_group.user_set.add(user)
        else:
            employee_group = Group.objects.get(name="Employee")
            employee_group.user_set.add(user)
            profile = Profile.objects.filter(user=user).first()
            profile.company = company
        messages.success(request, f"Account created for {user.username}")
        return redirect("login")

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        form = CreateUserForm()
        context = {"form": form, "title": "Register"}
        return render(request, "users/authorization/register.html", context)





# from django.contrib import messages
# from django.contrib.auth.models import Group
# from django.shortcuts import redirect, render
# from django.views.generic import View
#
# from recruitment.models import Company
# from users.forms import CreateUserForm
# from users.models import Profile


# class RegisterView(View):
#     def post(self, request):
#         form = CreateUserForm(request.POST)
#         if not form.is_valid():
#             return render(
#                 request, "users/register.html", {"form": form, "title": "Register"}
#             )
#
#         user = form.save()
#         username = user.username
#         email_domain = user.email.split(sep="@")[-1]
#         company = Company.objects.filter(email_domain=email_domain).first()
#         if company is None:
#             candidate_group = Group.objects.get(name="Candidate")
#             candidate_group.user_set.add(user)
#         else:
#             employee_group = Group.objects.get(name="Employee")
#             employee_group.user_set.add(user)
#             profile = Profile.objects.filter(user=user).first()
#             profile.company = company
#         messages.success(request, f"Account created for {user.username}")
#         return redirect("login")
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect("dashboard")
#         form = CreateUserForm()
#         context = {"form": form, "title": "Register"}
#         return render(request, "users/register.html", context)
