from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.views.generic import UpdateView

from users.forms import UserInfoEditByOwnerForm, AdminEditFormSet
from dashboards.views.dashboard_owner import UserHasOwnerOrHigherGroup
from users.models import Profile


class UserInfoEditByOwner(UserHasOwnerOrHigherGroup, UpdateView):
    model = User
    template_name = "users/profile/profile_edit_by_owner.html"
    form_class = UserInfoEditByOwnerForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['admin_edit_formset'] = AdminEditFormSet(self.request.POST, instance=self.object)
        else:
            data['admin_edit_formset'] = AdminEditFormSet(instance=self.object)
        return data

    def get_initial(self):
        initial = super(UserInfoEditByOwner, self).get_initial()
        current_group = self.object.groups.get()
        initial["group"] = current_group.pk
        return initial

    def form_valid(self, form):
        context = self.get_context_data()
        admin_edit_formset = context['admin_edit_formset']
        self.object.groups.clear()
        self.object.groups.add(form.cleaned_data["group"])
        self.object = form.save()
        if admin_edit_formset.is_valid():
            admin_edit_formset.instance = self.get_object()
            admin_edit_formset.save()
        return super(UserInfoEditByOwner, self).form_valid(form)

    def get_success_url(self):
        return reverse("profile", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        messages.success(request, f"User information successfully updated.")
        return super().post(request, *args, *kwargs)
















# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.shortcuts import reverse
# from django.views.generic import UpdateView
#
# from users.forms import UserProfileForm
# from dashboards.views.dashboard_owner import UserHasOwnerOrHigherGroup


# class UserInfoEditByOwner(UserHasOwnerOrHigherGroup, UpdateView):
#     model = User
#     template_name = "users/profile_edit_by_owner.html"
#     form_class = UserProfileForm
#
#     def get_initial(self):
#         initial = super(UserInfoEditByOwner, self).get_initial()
#         current_group = self.object.groups.get()
#         initial["group"] = current_group.pk
#         initial["phone_number"] = self.request.user.profile.phone_number
#         return initial
#
#     def form_valid(self, form):
#         self.object.groups.clear()
#         self.object.groups.add(form.cleaned_data["group"])
#         return super(UserInfoEditByOwner, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse("profile", kwargs={"pk": self.object.id})
#
#     def post(self, request, *args, **kwargs):
#         messages.success(request, f"User information successfully updated.")
#         return super().post(request, *args, *kwargs)
