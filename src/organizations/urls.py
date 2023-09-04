from django.urls import path

from organizations.views import RegisterCompanyView, CompanyProfileView

urlpatterns = [
    path(
        "register/", RegisterCompanyView.as_view(), name="register-company"),
    path(
        "company-profile/", CompanyProfileView.as_view(), name="company-profile"
    )
]
