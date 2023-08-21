from django.urls import path

from employee.views import EmployeeDashboardView

urlpatterns = [
    path("", EmployeeDashboardView.as_view(), name="employee-dashboard"),
]
