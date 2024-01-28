from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.views.generic import DetailView

from core.base import redirect_to_dashboard_based_on_group
from users.models import Profile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = "users/profile/profile_detail.html"
    model = Profile
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = User.objects.get(id=self.object.id)
        context[
            "title"
        ] = f"Profile - {user.first_name} {user.last_name} from {user.profile.company.name} - CloudStaffHub"
        return context

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_success_url(self):
        return reverse("profile", kwargs={"pk": self.object.id})
