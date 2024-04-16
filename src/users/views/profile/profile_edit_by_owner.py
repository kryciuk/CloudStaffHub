from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.views.generic import UpdateView

from core.base import redirect_to_dashboard_based_on_group
from organizations.models import Department, Position
from users.forms import AdminEditFormSet, UserInfoEditByOwnerForm


class UserInfoEditByOwnerView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    permission_required = "users.change_profile"
    template_name = "users/profile/profile_edit_by_owner.html"
    form_class = UserInfoEditByOwnerForm

    def get_queryset(self):
        return User.objects.filter(profile__company=self.request.user.profile.company)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        formset = AdminEditFormSet(instance=self.object)
        for form in formset:
            form.fields["department"].queryset = Department.objects.filter(company=self.object.profile.company)
            form.fields["position"].queryset = Position.objects.filter(company=self.object.profile.company)
        data["admin_edit_formset"] = formset
        data["title"] = f"Edit Profile {self.object.first_name} {self.object.last_name} - CloudStaffHub"
        return data

    def get_initial(self):
        initial = super(UserInfoEditByOwnerView, self).get_initial()
        current_group = self.object.groups.get()
        initial["group"] = current_group.pk
        return initial

    def form_valid(self, form):
        admin_edit_formset = AdminEditFormSet(self.request.POST, instance=self.object)
        self.object.groups.clear()
        self.object.groups.add(form.cleaned_data["group"])
        self.object = form.save()
        if admin_edit_formset.is_valid():
            admin_edit_formset.instance = self.get_object()
            admin_edit_formset.save()
        messages.success(self.request, "User information successfully updated.")
        return super(UserInfoEditByOwnerView, self).form_valid(form)

    def get_success_url(self):
        return reverse("profile-edit", kwargs={"pk": self.object.id})
