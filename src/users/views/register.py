from django.contrib import messages
from django.contrib.auth.models import User
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
                request, "users/register.html", {"form": form, "title": "Register"}
            )

        user = form.save()
        # username = user.username
        # email_domain = user.email.split(sep="@")[-1]
        # company = Company.objects.filter(email_domain=email_domain).first()
        # Profile.objects.create(user=user, company=company)
        messages.success(request, f"Account created for {user.username}")
        return redirect("login")

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        form = CreateUserForm()
        context = {"form": form, "title": "Register"}
        return render(request, "users/register.html", context)
