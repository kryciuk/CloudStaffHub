from django.views.generic import ListView

from recruitment.filters import JobOfferFilter
from recruitment.models import JobOffer


class JobOffersListView(ListView):
    model = JobOffer
    template_name = "recruitment/job_offers/job_offers.html"
    context_object_name = "job_offers"
    ordering = ["-status", "-published_date"]
    paginate_by = 5

    def get_queryset(self):  # napisać fancy
        company = self.request.user.profile.company
        queryset = JobOffer.objects.filter(status=True)
        if company is not None:
            queryset = JobOffer.objects.filter(company=company, status=True)
        self.filterset = JobOfferFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filterset.form
        return context
