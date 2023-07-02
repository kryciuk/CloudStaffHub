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
    path(
        "", CandidateDefaultView.as_view(), name="candidate_default"
    ),  # - instead of _
    path("job-offers", JobOffersView.as_view(), name="job_offers"),
    path("job-offer/<int:pk>", JobOfferView.as_view(), name="job_offer_detail"),
    path(
        "job-offer/update/<int:pk>", JobOfferUpdate.as_view(), name="job_offer_update"
    ),
    path("job-offer/create", JobOfferCreate.as_view(), name="job_offer_create"),
    path("job-offer/apply", ApplyJobOffer.as_view(), name="job_application"),
]
