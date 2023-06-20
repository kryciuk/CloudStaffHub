from django.urls import path
from recruitment.views import CandidateDefaultView, JobOffersView, JobOfferUpdate, JobOfferView

urlpatterns = [
    path('', CandidateDefaultView.as_view(), name='candidate_default'),
    path('job-offers', JobOffersView.as_view(), name='job_offers'),
    path('job-offer/<int:pk>', JobOfferView.as_view(), name='job_offer_detail'),
    path('job-offer/update/<int:pk>', JobOfferUpdate.as_view(), name='job_offer_update'),
        ]
