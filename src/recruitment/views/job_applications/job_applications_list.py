import django_filters
from django.views.generic import ListView

from recruitment.models import JobApplication


class JobApplicationsView(ListView):
    model = JobApplication
    template_name = "recruitment/job_applications/job_applications.html"
    context_object_name = "job_applications"
    ordering = ["-id"]
    queryset = JobApplication.objects.filter(status=JobApplication.Status.RECEIVED)
    paginate_by = 5


