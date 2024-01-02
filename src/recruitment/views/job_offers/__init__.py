from .job_offers_apply import JobOffersApplyView
from .job_offers_create import JobOffersCreateView, load_cities
from .job_offers_detail import JobOffersDetailView
from .job_offers_list import JobOffersListView
from .job_offers_update import JobOffersUpdateView

__all__ = [
    "JobOffersListView",
    "JobOffersApplyView",
    "JobOffersCreateView",
    "JobOffersDetailView",
    "JobOffersUpdateView",
    "load_cities",
]
