from django.views.generic import TemplateView


class ManagerDashboardView(TemplateView):
    template_name = "manager/manager_dashboard.html"


