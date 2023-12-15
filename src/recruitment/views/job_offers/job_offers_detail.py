from django.views.generic import DetailView

from recruitment.models import JobOffer, JobApplication


class JobOffersDetailView(DetailView):
    model = JobOffer
    template_name = "recruitment/job_offers/job_offer_detail.html"
    context_object_name = "job_offer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_application = JobApplication.objects.filter(candidate=self.request.user, job_offer=self.object)
        if user_application.exists():
            context['user_application'] = True
        else:
            context['user_application'] = False
        context['title'] = f"Job Offer ID{self.object.id} - CloudStaffHub"
        return context
