from django.views.generic import CreateView

from recruitment.forms import JobApplicationForm
from recruitment.models import JobOffer


class ApplyJobOffer(CreateView):
    form_class = JobApplicationForm
    template_name = "recruitment/job_offer_apply.html"
    context_object_name = "job_application"

    def form_valid(self, form):
        form.instance.job_offer = JobOffer.objects.get(pk=self.kwargs.get("pk"))
        if self.request.user.is_authenticated:
            form.instance.candidate = self.request.user
        return super().form_valid(form)
