from django.urls import path

from creator.views import CompanyAdminView

urlpatterns = [
    path("", CompanyAdminView.as_view(), name="company-admin-dashboard"),
]
