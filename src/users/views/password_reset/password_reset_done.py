from django.contrib.auth.views import PasswordResetDoneView


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset/password_reset_done.html"
