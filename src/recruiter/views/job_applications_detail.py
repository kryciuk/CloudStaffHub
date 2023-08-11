from django.views.generic import DetailView, UpdateView

from recruitment.models import JobApplication
from recruiter.forms import JobApplicationForm


class JobApplicationsDetailView(UpdateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = "recruiter/job_applications_detail.html"
    context_object_name = "job_application"

    def get_form_class(self):
        return JobApplicationForm
