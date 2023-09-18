from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from organizations.models import City
from recruitment.forms import JobOfferForm
from recruitment.models import Position


class JobOffersCreateView(LoginRequiredMixin, CreateView):
    form_class = JobOfferForm
    template_name = "recruitment/job_offers/job_offer_update.html"
    context_object_name = "job_offer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"].fields["position"].queryset = Position.objects.filter(
            company=self.request.user.profile.company
        ).order_by("title")
        context["form"].fields["city"].queryset = City.objects.all().order_by("name")
        return context

    def form_valid(self, form):
        form.instance.company = self.request.user.profile.company
        form.instance.published_date = datetime.now()
        return super().form_valid(form)
