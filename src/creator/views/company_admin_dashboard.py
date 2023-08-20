from django.contrib.auth.models import User
from django.views.generic import TemplateView


class CompanyAdminView(TemplateView):
    template_name = "creator/company_admin_dashboard.html"
    # permission_required = "Creator"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.user.profile.company
        context["employees"] = User.objects.filter(profile__company=company).order_by('-id')[:10]
        return context