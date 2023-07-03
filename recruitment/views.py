from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from .forms import JobApplicationForm, JobOfferForm
from .models import JobOffer


class CandidateDefaultView(View):
    template_name = "recruitment/candidate.html"

    def get(self, request):
        context = {"title": "Candidate"}
        return render(request, self.template_name, context)


class JobOffersView(ListView):
    model = JobOffer
    template_name = "recruitment/job_offers.html"
    context_object_name = "job_offers"
    ordering = ["-status", "-published_date"]
    paginate_by = 5


class JobOfferView(DetailView):
    model = JobOffer
    template_name = "recruitment/job_offer_detail.html"
    context_object_name = "job_offer"


class JobOfferUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "recruitment.change_joboffer"

    model = JobOffer
    form_class = JobOfferForm
    template_name = "recruitment/job_offer_update.html"
    context_object_name = "job_offer"


class JobOfferCreate(PermissionRequiredMixin, CreateView):
    permission_required = "recruitment.add_joboffer"

    form_class = JobOfferForm
    template_name = "recruitment/job_offer_update.html"
    context_object_name = "job_offer"


class ApplyJobOffer(CreateView):
    form_class = JobApplicationForm
    template_name = "recruitment/job_offer_apply.html"
    context_object_name = "job_application"

    def form_valid(self, form):
        form.instance.job_offer = JobOffer.objects.get(pk=self.kwargs.get("pk"))
        if self.request.user.is_authenticated:
            form.instance.candidate = self.request.user
        return super().form_valid(form)
