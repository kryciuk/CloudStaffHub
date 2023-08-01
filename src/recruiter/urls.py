from django.urls import path

from recruiter.views.city_create import CityCreate
from recruiter.views.position_create import PositionCreate
from recruiter.views.recruiter_default import RecruiterDefaultView

urlpatterns = [
    path("", RecruiterDefaultView.as_view(), name="recruiter-default"),
    path("position-create", PositionCreate.as_view(), name="position-create"),
    path("city-create", CityCreate.as_view(), name="city-create")
]
