from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView

from core.base import redirect_to_dashboard_based_on_group
from recruitment.forms import JobOfferFormUpdate
from recruitment.models import JobOffer


class JobOffersUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "recruitment.change_joboffer"
    model = JobOffer
    form_class = JobOfferFormUpdate
    template_name = "recruitment/job_offers/job_offer_update.html"
    context_object_name = "job_offer"

    def get_queryset(self):
        return JobOffer.objects.filter(company=self.request.user.profile.company)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Job Offer Update - CloudStaffHub"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Job offer was updated.")
        return super().form_valid(form)
