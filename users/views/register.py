from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from users.forms import CreateUserForm


class RegisterView(View):
    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {user}")
            return redirect("login")
        context = {"form": form, "title": "Register"}
        return render(request, "users/register.html", context)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        form = CreateUserForm()
        context = {"form": form, "title": "Register"}
        return render(request, "users/register.html", context)
