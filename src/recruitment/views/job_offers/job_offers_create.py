from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from recruitment.forms import JobOfferForm


class JobOffersCreateView(LoginRequiredMixin, CreateView):
    form_class = JobOfferForm
    template_name = "recruitment/job_offers/job_offer_update.html"
    context_object_name = "job_offer"

    def form_valid(self, form):
        form.instance.company = self.request.user.profile.company
        return super().form_valid(form)
