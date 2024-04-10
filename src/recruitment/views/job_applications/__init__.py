from .job_applications_approved import JobApplicationsApprovedView
from .job_applications_closed import JobApplicationsClosedView
from .job_applications_detail import JobApplicationsDetailView
from .job_applications_list import JobApplicationsView
from .job_applications_set_status import (
    JobApplicationsSetStatusApprovedView,
    JobApplicationsSetStatusClosedView,
    JobApplicationsSetStatusUnderReviewView,
)
from .job_applications_under_review import JobApplicationsUnderReviewView

__all__ = [
    "JobApplicationsApprovedView",
    "JobApplicationsClosedView",
    "JobApplicationsDetailView",
    "JobApplicationsView",
    "JobApplicationsSetStatusApprovedView",
    "JobApplicationsSetStatusClosedView",
    "JobApplicationsSetStatusUnderReviewView",
    "JobApplicationsUnderReviewView",
]
