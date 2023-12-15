import django_filters
from django.views.generic import ListView

from recruitment.models import JobApplication


class JobApplicationsView(ListView):
    model = JobApplication
    template_name = "recruitment/job_applications/job_applications.html"
    context_object_name = "job_applications"
    paginate_by = 5

    def get_queryset(self):
        return JobApplication.objects.filter(job_offer__company=self.request.user.profile.company,
                                             status=JobApplication.Status.RECEIVED).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Job Applications - CloudStaffHub"
        return context