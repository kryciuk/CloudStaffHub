from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.views.generic import CreateView

from organizations.models import Department
from recruiter.forms import PositionsForm


class PositionCreateView(UserPassesTestMixin, CreateView):
    form_class = PositionsForm
    template_name = "recruiter/positions_create.html"
    context_object_name = "position"

    def test_func(self):
        user_groups = ["Recruiter", "Manager", "Owner"]
        return self.request.user.is_authenticated and (
            self.request.user.groups.filter(name__in=user_groups).exists() or self.request.user.is_superuser
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"].fields["department"].queryset = Department.objects.filter(
            company=self.request.user.profile.company
        )
        return context

    def form_valid(self, form):
        form.instance.company = self.request.user.profile.company
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.session.get("previous_view") == "JobOffersCreateView":
            self.request.session["previous_view"] = None
            return reverse("job-offer-create")
        return reverse("dashboard-recruiter")
