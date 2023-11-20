from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views.generic import DetailView

from users.models import Profile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = "users/profile/profile_detail.html"
    model = Profile
    context_object_name = "profile"

    def get_success_url(self):
        return reverse("profile", kwargs={"pk": self.object.id})
