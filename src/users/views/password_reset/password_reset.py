from django.contrib.auth.views import PasswordResetView


class UserPasswordResetView(PasswordResetView):
    template_name = "users/password_reset/password_reset.html"
    html_email_template_name = "users/password_reset/password_message.html"

    def get(self, request, *args, **kwargs):
        request.session["previous_view"] = "UserPasswordResetView"
        return super().get(request, *args, **kwargs)