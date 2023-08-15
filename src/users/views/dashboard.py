from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        context = {"title": "Dashboard"}
        return render(request, "users/dashboard.html", context)