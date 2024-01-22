from django.urls import path

from organizations.views import CompanyProfileView, RegisterCompanyView

urlpatterns = [
    path("register/", RegisterCompanyView.as_view(), name="register-company"),
    path("company-profile/<int:pk>", CompanyProfileView.as_view(), name="company-profile"),
]
