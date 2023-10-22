from django.contrib.auth.views import PasswordResetView


class UserPasswordResetView(PasswordResetView):
    template_name = "users/password_reset/password_reset.html"
    html_email_template_name = "users/password_reset/password_message.html"