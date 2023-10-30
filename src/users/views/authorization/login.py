from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from core.base import has_group


class UserLoginView(LoginView):
    template_name = "users/authorization/login.html"
    success_url = reverse_lazy('profile')

    def form_invalid(self, form):
        messages.warning(self.request, "Your login details are incorrect.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Logged in successfully. Welcome to CloudStaffHub.")
        return super().form_valid(form)

    def get_success_url(self):
        if has_group(self.request.user, "Candidate"):
            return reverse_lazy('dashboard-candidate')
        return reverse_lazy('dashboard-employee')