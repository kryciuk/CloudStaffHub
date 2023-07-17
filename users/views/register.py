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
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            domain = form.cleaned_data.get("email").rsplit(sep="@")[-1]
            company = Company.objects.filter(email_domain=domain).first()
            user1 = User.objects.get(username=username)
            profile = Profile(user=user1, company=company)
            profile.save()
            messages.success(request, f"Account created for {username}")
            return redirect("login")
        context = {"form": form, "title": "Register"}
        return render(request, "users/register.html", context)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        form = CreateUserForm()
        context = {"form": form, "title": "Register"}
        return render(request, "users/register.html", context)
