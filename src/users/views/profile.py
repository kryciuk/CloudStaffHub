from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.views.generic import UpdateView

from users.forms import UserProfileForm, UserProfileFormChange
from users.models import Profile


class ProfileDetailView(UpdateView):
    template_name = "users/profile.html"
    model = Profile
    form_class = UserProfileFormChange

    def get_success_url(self):
        return reverse("profile", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        messages.success(request, f"Profile updated")
        return super().post(request, *args, *kwargs)


class UserProfileUpdateView(UpdateView):
    model = User
    template_name = "users/profile_edit.html"
    form_class = UserProfileForm

    def get_initial(self):
        initial = super(UserProfileUpdateView, self).get_initial()
        try:
            current_group = self.object.groups.get()
        except:
            # exception can occur if the edited user has no groups
            # or has more than one group
            pass
        else:
            initial["group"] = current_group.pk
        return initial

    def form_valid(self, form):
        self.object.groups.clear()
        self.object.groups.add(form.cleaned_data["group"])
        return super(UserProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("profile", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        messages.success(request, f"User Information Updated")
        return super().post(request, *args, *kwargs)
