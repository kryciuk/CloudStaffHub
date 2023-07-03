from django.contrib.auth import logout
from django.shortcuts import render
from django.views.generic import View


class LogoutView(View):
    def get(self, request):
        logout(request)
        context = {"title": "Logout"}
        return render(request, "users/logout.html", context)
