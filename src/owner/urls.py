from django.urls import path

from owner.views.department_create import DepartmentCreateView

urlpatterns_departments = [
    path("departments/create", DepartmentCreateView.as_view(), name="department-create"),
]

urlpatterns = []

urlpatterns += urlpatterns_departments
