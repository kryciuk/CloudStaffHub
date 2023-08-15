# from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, View


class RecruiterDefaultView(TemplateView):             #PermissionRequiredMixin,
    template_name = "recruiter/recruiter_default.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Recruiter"
        return context

