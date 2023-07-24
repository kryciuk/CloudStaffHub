from django.shortcuts import render
from django.views.generic import View


class CandidateDefaultView(View):
    template_name = "recruitment/candidate.html"

    def get(self, request):
        context = {"title": "Candidate"}
        return render(request, self.template_name, context)
