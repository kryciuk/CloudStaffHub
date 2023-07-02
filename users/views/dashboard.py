from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        context = {"title": "Dashboard"}
        return render(request, "users/dashboard.html", context)
