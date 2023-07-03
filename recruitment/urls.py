from django.urls import path

from recruitment.views.candidate_default import CandidateDefaultView
from recruitment.views.job_offers_apply import ApplyJobOffer
from recruitment.views.job_offers_create import JobOfferCreate
from recruitment.views.job_offers_detail import JobOfferView
from recruitment.views.job_offers_list import JobOffersView
from recruitment.views.job_offers_update import JobOfferUpdate

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
