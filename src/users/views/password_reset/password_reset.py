from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from users.forms import PasswordResetFormCustom


class UserPasswordResetView(PasswordResetView):
    template_name = "users/password_reset/password_reset.html"
    html_email_template_name = "users/password_reset/password_message.html"
    form_class = PasswordResetFormCustom
    subject_template_name = "users/password_reset/password_reset_subject.txt"

    def get(self, request, *args, **kwargs):
        request.session["previous_view"] = "UserPasswordResetView"
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)