from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.views.generic import UpdateView

from organizations.models import CompanyProfile
from users.forms import UserProfileUpdateForm


class CompanyProfileView(UpdateView):
    template_name = "organizations/company_profile.html"
    model = CompanyProfile
    fields = "__all__"

    def get_success_url(self):
        return reverse("profile", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        messages.success(request, f"Company profile updated")
        return super().post(request, *args, *kwargs)


# class UserProfileUpdateView(UpdateView):
#     model = User
#     template_name = "users/profile_edit.html"
#
#     def get_initial(self):
#         initial = super(UserProfileUpdateView, self).get_initial()
#         try:
#             current_group = self.object.groups.get()
#         except:
#             # exception can occur if the edited user has no groups
#             # or has more than one group
#             pass
#         else:
#             initial["group"] = current_group.pk
#         return initial
#
#     def get_form_class(self):
#         return UserProfileForm
#
#     def form_valid(self, form):
#         self.object.groups.clear()
#         self.object.groups.add(form.cleaned_data["group"])
#         return super(UserProfileUpdateView, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse("profile", kwargs={"pk": self.object.id})
#
#     def post(self, request, *args, **kwargs):
#         messages.success(request, f"User information updated")
#         return super().post(request, *args, *kwargs)
