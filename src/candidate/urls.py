from django.urls import path

from candidate.views import CandidateDashboardView

urlpatterns = [
    path("", CandidateDashboardView.as_view(), name="candidate-dashboard"),
]