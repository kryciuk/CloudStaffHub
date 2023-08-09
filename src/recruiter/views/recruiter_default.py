from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import View, TemplateView


class RecruiterDefaultView(PermissionRequiredMixin, TemplateView):
    template_name = "recruiter/recruiter_default.html"
    permission_required = "recruiter"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Recruiter"
        return context

    # def get(self, request):
    #     context = {"title": "Recruiter"}
    #     return render(request, self.template_name, context)
