from django.urls import path

from .views import (
    DepartmentCreateView,
    DepartmentDeleteView,
    DepartmentListView,
    EmployeesListView,
)

urlpatterns_departments = [
    path("departments/create", DepartmentCreateView.as_view(), name="department-create"),
    path("departments/list", DepartmentListView.as_view(), name="department-list"),
    path("departments/<int:pk>/delete", DepartmentDeleteView.as_view(), name="department-delete"),
]

urlpatterns_employees = [
    path("employees", EmployeesListView.as_view(), name="employee-list"),
]

urlpatterns = []

urlpatterns += urlpatterns_departments + urlpatterns_employees
