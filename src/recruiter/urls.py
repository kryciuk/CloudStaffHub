from django.urls import path

from recruiter.views.city_create import CityCreate
from recruiter.views.job_applications_closed import JobApplicationsClosedView
from recruiter.views.job_applications_list import JobApplicationsView
from recruiter.views.position_create import PositionCreate
from recruiter.views.recruiter_default import RecruiterDefaultView
from recruiter.views.job_applications_under_review import JobApplicationsUnderReviewView
from recruiter.views.job_applications_detail import JobApplicationsDetailView

urlpatterns = [
    path("", RecruiterDefaultView.as_view(), name="recruiter-default"),
    path("position-create", PositionCreate.as_view(), name="position-create"),
    path("city-create", CityCreate.as_view(), name="city-create"),
    path("job-applications", JobApplicationsView.as_view(), name="job-applications"),
    path("job-applications-closed", JobApplicationsClosedView.as_view(), name="job-applications-closed"),
    path("job-applications-review", JobApplicationsUnderReviewView.as_view(), name="job-applications-review"),
    path("job-applications-detail/<int:pk>", JobApplicationsDetailView.as_view(), name="job-applications-detail"),
]
