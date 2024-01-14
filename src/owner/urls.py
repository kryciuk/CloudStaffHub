from django.urls import path

from .views import DepartmentCreateView, DepartmentDeleteView, DepartmentListView

urlpatterns_departments = [
    path("departments/create", DepartmentCreateView.as_view(), name="department-create"),
    path("departments/list", DepartmentListView.as_view(), name="department-list"),
    path("departments/delete/<int:pk>", DepartmentDeleteView.as_view(), name="department-delete"),
]

urlpatterns = []

urlpatterns += urlpatterns_departments
