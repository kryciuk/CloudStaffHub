from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class RecruiterDefaultView(PermissionRequiredMixin, View):
    template_name = "recruiter/recruiter_default.html"
    permission_required = "recruiter"

    def get(self, request):
        context = {"title": "Recruiter"}
        return render(request, self.template_name, context)
