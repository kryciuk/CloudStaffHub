from django.urls import path

from dashboards.views import (
    CandidateDashboardView,
    EmployeeDashboardView,
    ManagerDashboardView,
    OwnerDashboardView,
    RecruiterDashboardView,
)

urlpatterns = [
    path("candidate/", CandidateDashboardView.as_view(), name="dashboard-candidate"),
    path("owner/", OwnerDashboardView.as_view(), name="dashboard-owner"),
    path("employee/", EmployeeDashboardView.as_view(), name="dashboard-employee"),
    path("manager/", ManagerDashboardView.as_view(), name="dashboard-manager"),
    path("recruiter/", RecruiterDashboardView.as_view(), name="dashboard-recruiter"),
]
