from django.views.generic import TemplateView


class CandidateDefaultView(TemplateView):
    template_name = "recruitment/candidate.html"


