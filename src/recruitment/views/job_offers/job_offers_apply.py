from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView

from core.base import redirect_to_dashboard_based_on_group
from recruitment.forms import JobApplicationForm
from recruitment.models import JobOffer


class JobOffersApplyView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = JobApplicationForm
    permission_required = "recruitment.add_jobapplication"
    template_name = "recruitment/job_offers/job_offer_apply.html"
    context_object_name = "job_application"

    def get(self, request, *args, **kwargs):
        job_offer = JobOffer.objects.filter(pk=kwargs.get("pk")).first()
        if job_offer and not job_offer.status:
            raise Http404("A job offer with this ID does not exist.")
        return super().get(request, *args, **kwargs)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_initial(self):
        initial = super(JobOffersApplyView, self).get_initial()
        initial = initial.copy()
        initial["first_name"] = self.request.user.first_name
        initial["last_name"] = self.request.user.last_name
        initial["email"] = self.request.user.email

        phone_number = self._get_phone_number()
        if phone_number:
            initial["phone_number"] = phone_number
        return initial

    def _get_phone_number(self):
        phone_number = self.request.user.profile.phone_number
        if phone_number is None:
            return False

        return phone_number

    def form_valid(self, form):
        try:
            obj = get_object_or_404(JobOffer, pk=self.kwargs.get("pk"))
        except JobOffer.DoesNotExist:
            raise Http404("A job offer with this ID does not exist.")
        form.instance.job_offer = obj
        if self.request.user.is_authenticated:
            form.instance.candidate = self.request.user
        messages.success(self.request, "The application was sent.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job_offer"] = get_object_or_404(JobOffer, pk=self.kwargs.get("pk"))
        context["title"] = "Job Offer Apply - CloudStaffHub"
        return context
