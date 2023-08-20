from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView

from recruitment.forms import JobApplicationForm
from recruitment.models import JobOffer


class JobOffersApplyView(CreateView):
    form_class = JobApplicationForm
    template_name = "recruitment/job_offers/job_offer_apply.html"
    context_object_name = "job_application"

    def form_valid(self, form):
        try:
            obj = get_object_or_404(JobOffer, pk=self.kwargs.get("pk"))
        except JobOffer.DoesNotExist:
            raise Http404("A job offer with this ID does not exist.")
        form.instance.job_offer = obj
        if self.request.user.is_authenticated:
            form.instance.candidate = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_offer'] = get_object_or_404(JobOffer, pk=self.kwargs.get("pk"))
        return context
