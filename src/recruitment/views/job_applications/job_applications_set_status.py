from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from recruitment.forms import JobApplicationStatusForm
from recruitment.models import JobApplication


class JobApplicationsSetStatusUnderReviewView(UpdateView):
    model = JobApplication
    form_class = JobApplicationStatusForm
    context_object_name = "job_application"
    success_url = reverse_lazy("job-applications")

    def form_valid(self, form):
        form.instance.status = 1
        return super().form_valid(form)


class JobApplicationsSetStatusClosedView(UpdateView):
    model = JobApplication
    form_class = JobApplicationStatusForm
    context_object_name = "job_application"
    success_url = reverse_lazy("job-applications")

    def form_valid(self, form):
        form.instance.status = 2
        return super().form_valid(form)
