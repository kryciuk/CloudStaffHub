from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import UpdateView

from recruitment.forms import JobOfferFormUpdate
from recruitment.models import JobOffer


class JobOffersUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "recruitment.change_joboffer"

    model = JobOffer
    form_class = JobOfferFormUpdate
    template_name = "recruitment/job_offers/job_offer_update.html"
    context_object_name = "job_offer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Job Offer Update - CloudStaffHub"
        return context
