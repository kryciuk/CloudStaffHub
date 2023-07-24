from django.views.generic import ListView

from recruitment.models import JobOffer


class JobOffersView(ListView):
    model = JobOffer
    template_name = "recruitment/job_offers.html"
    context_object_name = "job_offers"
    ordering = ["-status", "-published_date"]
    paginate_by = 5
