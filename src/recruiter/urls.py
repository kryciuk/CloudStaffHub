from django.urls import path

from recruiter.views.city_create import CityCreateView
from recruiter.views.position_create import PositionCreateView
from recruiter.views.recruiter_dashboard import RecruiterDashboardView

urlpatterns = [
    path("", RecruiterDashboardView.as_view(), name="recruiter-dashboard"),
    path("position-create", PositionCreateView.as_view(), name="position-create"),
    path("city-create", CityCreateView.as_view(), name="city-create"),
]
