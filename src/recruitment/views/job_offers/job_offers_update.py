from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView

from recruitment.forms import JobOfferFormUpdate
from recruitment.models import JobOffer


class JobOffersUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = "recruitment.change_joboffer"
    model = JobOffer
    form_class = JobOfferFormUpdate
    template_name = "recruitment/job_offers/job_offer_update.html"
    context_object_name = "job_offer"

    def test_func(self):
        job_offer = self.get_object()
        return self.request.user.is_authenticated and (
                self.request.user.profile.company == job_offer.company)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Job Offer Update - CloudStaffHub"
        return context
