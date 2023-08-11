from django.views.generic import ListView

from recruitment.models import JobApplication


class JobApplicationsView(ListView):
    model = JobApplication
    template_name = "recruiter/job_applications.html"
    context_object_name = "job_applications"
    ordering = ["-id"]
    queryset = JobApplication.objects.filter(status=0)
    paginate_by = 5
