from django.urls import path
from recruitment.views import (
    CandidateDefaultView,
    JobOffersView,
    JobOfferUpdate,
    JobOfferView,
    JobOfferCreate,
    ApplyJobOffer,
)

urlpatterns = [
    path("", CandidateDefaultView.as_view(), name="candidate-default"),
    path("job-offers", JobOffersView.as_view(), name="job-offers"),
    path("job-offers/<int:pk>", JobOfferView.as_view(), name="job-offer-detail"),
    path(
        "job-offers/update/<int:pk>", JobOfferUpdate.as_view(), name="job-offer-update"
    ),
    path("job-offers/create", JobOfferCreate.as_view(), name="job-offer-create"),
    path("job-offers/apply/<int:pk>", ApplyJobOffer.as_view(), name="job-offer-apply"),
]
