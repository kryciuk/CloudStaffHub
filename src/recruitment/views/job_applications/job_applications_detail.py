from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import UpdateView

from recruitment.forms import JobApplicationStatusForm
from recruitment.models import JobApplication


class JobApplicationsDetailView(UpdateView):
    model = JobApplication
    form_class = JobApplicationStatusForm
    template_name = "recruitment/job_applications/job_applications_detail.html"
    context_object_name = "job_application"

    def get_form_class(self):
        return JobApplicationStatusForm
