from django.urls import path

from organizations.views import RegisterCompanyView

urlpatterns = [
    path(
        "register/", RegisterCompanyView.as_view(), name="register-company"
    )  # 'organizations/register
]
