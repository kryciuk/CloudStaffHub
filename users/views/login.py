from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import View


class LoginView(View):
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.warning(request, "Your login details are incorrect")
        context = {"title": "Login"}
        return render(request, "users/login.html", context)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        context = {"title": "Login"}
        return render(request, "users/login.html", context)
