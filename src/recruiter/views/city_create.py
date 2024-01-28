from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView

from core.base import redirect_to_dashboard_based_on_group
from recruiter.forms import CityForm


class CityCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    form_class = CityForm
    template_name = "recruiter/city_create.html"
    context_object_name = "city"
    permission_required = "organizations.add_city"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add New City - CloudStaffHub"
        return context

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_success_url(self):
        if self.request.session.get("previous_view") == "JobOffersCreateView":
            self.request.session["previous_view"] = None
            return reverse("job-offer-create")
        return reverse("dashboard-recruiter")

    def form_valid(self, form):
        messages.success(self.request, "New city added to the database.")
        return super().form_valid(form)
