from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views.generic import DetailView

from core.base import redirect_to_dashboard_based_on_group
from users.models import Profile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = "users/profile/profile_detail.html"
    model = Profile
    context_object_name = "profile"

    def handle_no_permission(self):
        messages.warning(self.request, "You don't have the required permissions to access this page.")
        return redirect_to_dashboard_based_on_group("")

    def get_success_url(self):
        return reverse("profile", kwargs={"pk": self.object.id})
