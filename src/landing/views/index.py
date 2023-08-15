from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    def get(self, request):
        context = {"title": "Welcome"}
        return render(request, "landing/index.html", context)
