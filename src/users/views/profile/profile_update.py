from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import reverse
from django.views.generic import UpdateView

from users.forms import UserProfileUpdateForm
from users.models import Profile
from core.base import has_group


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "users/profile/profile_update.html"
    model = Profile
    form_class = UserProfileUpdateForm

    def get_success_url(self):
        return reverse("profile-update", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        messages.success(request, f"Profile successfully updated.")
        return super().post(request, *args, *kwargs)

    def test_func(self):
        return (self.kwargs.get("pk") == self.request.user.id) or has_group(self.request.user, "Owner")