from django.urls import path

from organizations.views import CompanyAdminView, RegisterCompanyView

urlpatterns = [
    path("admin/", CompanyAdminView.as_view(), name="company-admin"),  # 'organizations/admin
    path("register/", RegisterCompanyView.as_view(), name="register-company")  # 'organizations/register
]
