from django.shortcuts import render
from django.views.generic import View

from users.models import Profile

# class AdminCompanyView(ListView):
#     model = Profile
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         company_id = self.request.user.profile.company.id
#         return queryset.filter(company=company)


class CompanyAdminView(View):
    template_name = "organizations/company_admin.html"
    permission_required = "Creator"

    def get(self, request):
        company = request.user.profile.company
        company_users_profiles = Profile.objects.filter(company=company)
        users = []
        for profile in company_users_profiles:
            users.append(profile.user)
        context = {"title": "Admin Company", "users": users}
        return render(request, self.template_name, context)