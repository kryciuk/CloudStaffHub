from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView

from core.base import redirect_to_dashboard_based_on_group
from organizations.models import Department
from recruiter.forms import PositionsForm


class PositionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PositionsForm
    template_name = "recruiter/positions_create.html"
    permission_required = "organizations.add_position"
    context_object_name = "position"

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"].fields["department"].queryset = Department.objects.filter(
            company=self.request.user.profile.company
        )
        context["title"] = "Add New Position - CloudStaffHub"
        return context

    def form_valid(self, form):
        form.instance.company = self.request.user.profile.company
        messages.success(self.request, "New position added to the database.")
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.session.get("previous_view") == "JobOffersCreateView":
            self.request.session["previous_view"] = None
            return reverse("job-offer-create")
        return reverse("dashboard-recruiter")
