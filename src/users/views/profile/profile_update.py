from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views.generic import UpdateView

from users.forms import UserProfileUpdateForm
from users.models import Profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile/profile_update.html"
    model = Profile
    form_class = UserProfileUpdateForm
    permission_denied_message = "No access"

    def get_success_url(self):
        return reverse("profile", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        messages.success(request, f"Profile successfully updated.")
        return super().post(request, *args, *kwargs)
