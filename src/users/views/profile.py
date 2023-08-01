from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse
from django.views.generic import DetailView, UpdateView

from users.forms import UserProfileForm
# from users.forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from users.models import Profile


class ProfileDetailView(UpdateView):
    template_name = 'users/profile.html'
    model = Profile
    fields = ["phone_number", "company"]

    def get_success_url(self):
        return reverse('profile', kwargs={"pk": self.object.id})


class UserProfileUpdateView(UpdateView):
    model = User
    template_name = 'users/profile_edit.html'

    def get_initial(self):
        initial = super(UserProfileUpdateView, self).get_initial()
        try:
            current_group = self.object.groups.get()
        except:
            # exception can occur if the edited user has no groups
            # or has more than one group
            pass
        else:
            initial['group'] = current_group.pk
        return initial

    def get_form_class(self):
        return UserProfileForm

    def form_valid(self, form):
        self.object.groups.clear()
        self.object.groups.add(form.cleaned_data['group'])
        return super(UserProfileUpdateView, self).form_valid(form)
