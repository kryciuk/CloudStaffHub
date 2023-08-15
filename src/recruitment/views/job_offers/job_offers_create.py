from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView

from recruitment.forms import JobOfferForm


class JobOffersCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "recruitment.add_joboffer"

    form_class = JobOfferForm
    template_name = "recruitment/job_offers/job_offer_update.html"
    context_object_name = "job_offer"
