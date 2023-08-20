from django.urls import path

from manager.views import ManagerDashboardView

urlpatterns = [
    path("", ManagerDashboardView.as_view(), name="manager-dashboard"),
]
