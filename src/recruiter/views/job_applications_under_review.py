from django.views.generic import ListView

from recruitment.models import JobApplication


class JobApplicationsUnderReviewView(ListView):
    model = JobApplication
    template_name = "recruiter/job_applications_closed.html"
    context_object_name = "job_applications"
    queryset = JobApplication.objects.filter(status=1)
    paginate_by = 5
