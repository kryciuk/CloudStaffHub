from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.views.generic import UpdateView

from core.base import redirect_to_dashboard_based_on_group
from organizations.models import Department
from users.forms import AdminEditFormSet, UserInfoEditByOwnerForm


class UserInfoEditByOwnerView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    permission_required = "users.change_profile"
    template_name = "users/profile/profile_edit_by_owner.html"
    form_class = UserInfoEditByOwnerForm

    def handle_no_permission(self):
        messages.warning(self.request, "You don't have the required permissions to access this page.")
        if self.request.user.is_authenticated:
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        return redirect_to_dashboard_based_on_group("")

    def test_func(self):
        user = self.get_object()
        return self.request.user.profile.company == user.profile.company

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        formset = AdminEditFormSet(instance=self.object)
        for form in formset:
            form.fields["department"].queryset = Department.objects.filter(company=self.object.profile.company)
        data["admin_edit_formset"] = formset
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
        return super(UserInfoEditByOwnerView, self).form_valid(form)

    def get_success_url(self):
        return reverse("profile-edit", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        messages.success(request, "User information successfully updated.")
        return super().post(request, *args, *kwargs)
