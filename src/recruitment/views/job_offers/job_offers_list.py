from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.base import redirect_to_dashboard_based_on_group
from recruitment.filters import JobOfferFilter
from recruitment.models import JobOffer


class JobOffersListView(LoginRequiredMixin, ListView):
    model = JobOffer
    template_name = "recruitment/job_offers/job_offers.html"
    context_object_name = "job_offers"
    paginate_by = 5

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_queryset(self):  # napisać fancy
        company = self.request.user.profile.company
        queryset = JobOffer.objects.filter(status=True).order_by("-published_date")
        if company is not None:
            queryset = JobOffer.objects.filter(company=company, status=True).order_by("-published_date")
        self.filterset = JobOfferFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filterset.form
        context["title"] = "Job Offers - CloudStaffHub"
        return context
