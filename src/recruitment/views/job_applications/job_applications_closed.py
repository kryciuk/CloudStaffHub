from django.views.generic import ListView

from recruitment.models import JobApplication


class JobApplicationsClosedView(ListView):
    model = JobApplication
    template_name = "recruitment/job_applications/job_applications.html"
    context_object_name = "job_applications"
    queryset = JobApplication.objects.filter(status=JobApplication.Status.CLOSED).order_by("-id")
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Job Applications Closed - CloudStaffHub"
        return context