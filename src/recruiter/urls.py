from django.urls import path

from recruiter.views import CityCreateView
from recruiter.views.positions import (
    PositionCreateView,
    PositionDeleteView,
    PositionListView,
)

urlpatterns_positions = [
    path("positions/create", PositionCreateView.as_view(), name="positions-create"),
    path("positions/list", PositionListView.as_view(), name="positions-list"),
    path(
        "positions/delete/<int:pk>",
        PositionDeleteView.as_view(),
        name="positions-delete",
    ),
]

urlpatterns_cities = [
    path("city/create", CityCreateView.as_view(), name="city-create"),
]

urlpatterns = []

urlpatterns += urlpatterns_positions + urlpatterns_cities
