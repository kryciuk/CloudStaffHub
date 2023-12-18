from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView

from recruitment.forms import JobApplicationStatusForm
from recruitment.models import JobApplication


class JobApplicationsDetailView(UserPassesTestMixin, UpdateView):
    model = JobApplication
    form_class = JobApplicationStatusForm
    template_name = "recruitment/job_applications/job_applications_detail.html"
    context_object_name = "job_application"

    def test_func(self):
        job_application = self.get_object()
        return self.request.user.is_authenticated and (
            self.request.user.groups.filter(name="Recruiter").exists() or
            self.request.user.groups.filter(name="Manager").exists()
            or self.request.user.groups.filter(name="Owner").exists()
            or self.request.user.is_superuser
        ) and (self.request.user.profile.company == job_application.job_offer.company)

    def get_form_class(self):
        return JobApplicationStatusForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Job Application ID{self.object.id} - CloudStaffHub"
        return context