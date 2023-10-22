from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import reverse_lazy


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset/password_reset_complete.html"
