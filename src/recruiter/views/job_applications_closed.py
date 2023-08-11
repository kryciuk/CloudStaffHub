from django.views.generic import ListView

from recruitment.models import JobApplication


class JobApplicationsClosedView(ListView):
    model = JobApplication
    template_name = "recruiter/job_applications_closed.html"
    context_object_name = "job_applications"
    queryset = JobApplication.objects.filter(status=2)
    paginate_by = 5
