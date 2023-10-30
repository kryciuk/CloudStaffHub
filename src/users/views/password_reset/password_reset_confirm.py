from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset/password_reset_confirm.html"

    def get(self, request, *args, **kwargs):
        request.session["previous_view"] = "PasswordResetConfirmView"
        return super().get(request, *args, **kwargs)
