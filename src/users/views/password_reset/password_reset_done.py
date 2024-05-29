from django.contrib.auth.views import PasswordResetDoneView
from django.http import HttpResponseForbidden


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset/password_reset_done.html"

    def get(self, request, *args, **kwargs):
        if request.session["previous_view"] is None:
            return HttpResponseForbidden()
        request.session["previous_view"] = None
        return super().get(request, *args, **kwargs)
