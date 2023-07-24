from django.shortcuts import render
from django.views.generic import View


class WelcomeView(View):
    def get(self, request):
        context = {"title": "Welcome"}
        return render(request, "users/welcome.html", context)
