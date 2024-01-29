from django.urls import path

from .views.job_applications import (
    JobApplicationsClosedView,
    JobApplicationsDetailView,
    JobApplicationsSetStatusClosedView,
    JobApplicationsSetStatusUnderReviewView,
    JobApplicationsUnderReviewView,
    JobApplicationsView,
)
from .views.job_offers import (
    JobOffersApplyView,
    JobOffersCreateView,
    JobOffersDetailView,
    JobOffersListView,
    JobOffersUpdateView,
    load_cities,
)

urlpatterns = []

urlpatterns_job_offers = [
    path("job-offers", JobOffersListView.as_view(), name="job-offers"),
    path("job-offers/<int:pk>", JobOffersDetailView.as_view(), name="job-offer-detail"),
    path("job-offers/<int:pk>/update", JobOffersUpdateView.as_view(), name="job-offer-update"),
    path("job-offers/create", JobOffersCreateView.as_view(), name="job-offer-create"),
    path("job-offers/<int:pk>/apply", JobOffersApplyView.as_view(), name="job-offer-apply"),
]

urlpatterns_job_applications = [
    path("job-applications/received", JobApplicationsView.as_view(), name="job-applications"),
    path("job-applications/closed", JobApplicationsClosedView.as_view(), name="job-applications-closed"),
    path("job-applications/review", JobApplicationsUnderReviewView.as_view(), name="job-applications-review"),
    path("job-applications/<int:pk>/detail", JobApplicationsDetailView.as_view(), name="job-applications-detail"),
    path(
        "job-applications/<int:pk>/under-review",
        JobApplicationsSetStatusUnderReviewView.as_view(),
        name="job-applications-under-review",
    ),
    path(
        "job-applications/<int:pk>/close", JobApplicationsSetStatusClosedView.as_view(), name="job-applications-close"
    ),
    path("load_cities", load_cities, name="load-cities"),
]

urlpatterns += urlpatterns_job_offers + urlpatterns_job_applications
