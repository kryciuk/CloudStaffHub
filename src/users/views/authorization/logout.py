from django.contrib.auth.views import LogoutView
from django.contrib import messages


class UserLogoutView(LogoutView):
    template_name = "users/authorization/logout.html"

    def get(self, request, *args, **kwargs):
        messages.success(self.request, "Logged out successfully.")
        return super().get(request, *args, **kwargs)
