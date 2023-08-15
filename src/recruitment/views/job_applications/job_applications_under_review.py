from django.views.generic import ListView

from recruitment.models import JobApplication


class JobApplicationsUnderReviewView(ListView):
    model = JobApplication
    template_name = "recruitment/job_applications/job_applications_closed.html"
    context_object_name = "job_applications"
    queryset = JobApplication.objects.filter(status=JobApplication.Status.UNDER_REVIEW)
    paginate_by = 5
