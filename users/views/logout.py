from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import logout


class LogoutView(View):
    def get(self, request):
        logout(request)
        context = {"title": "Logout"}
        return render(request, "users/logout.html", context)
