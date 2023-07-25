from django.shortcuts import render
from django.views.generic import View


class EvaluationDashboard(View):
    template_name = "evaluation/dashboard.html"

    def get(self, request):
        context = {"title": "Evaluation"}
        return render(request, self.template_name, context)
