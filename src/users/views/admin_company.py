from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import View

from users.models import Profile


class AdminCompanyView(View):
    template_name = "users/admin_company.html"
    permission_required = "creator"

    def get(self, request):
        company = request.user.profile.company
        print(company)
        company_users_profiles = Profile.objects.filter(company=company)
        users = []
        for profile in company_users_profiles:
            users.append(profile.user)
        print(users)
        context = {"title": "Admin Company", "users": users}
        return render(request, self.template_name, context)