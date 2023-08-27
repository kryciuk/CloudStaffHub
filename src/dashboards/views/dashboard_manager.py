from django.views.generic import TemplateView


class ManagerDashboardView(TemplateView):
    template_name = "dashboards/dashboard_manager.html"
