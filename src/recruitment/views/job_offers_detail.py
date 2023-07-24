from django.views.generic import DetailView

from recruitment.models import JobOffer


class JobOfferView(DetailView):
    model = JobOffer
    template_name = "recruitment/job_offer_detail.html"
    context_object_name = "job_offer"
