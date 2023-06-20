from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, View
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import JobOffer

class CandidateDefaultView(View):
    def get(self, request):
        context = {'title': 'Candidate'}
        return render(request, 'recruitment/candidate.html', context)


class JobOffersView(ListView):
    model = JobOffer
    template_name = 'recruitment/job_offers.html'
    context_object_name = 'job_offers'
    ordering = ['-status', '-date_start']
    paginate_by = 5


class JobOfferView(DetailView):
    model = JobOffer
    template_name = 'recruitment/job_offer_detail.html'
    context_object_name = 'job_offer'


class JobOfferUpdate(PermissionRequiredMixin, UpdateView):

    permission_required = 'job_offer.change_joboffer'

    model = JobOffer
    template_name = 'recruitment/job_offer_update.html'
    context_object_name = 'job_offer'
    fields = '__all__'


