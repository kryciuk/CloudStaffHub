from django.contrib.auth.views import PasswordResetCompleteView
from django.http import HttpResponseForbidden


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset/password_reset_complete.html"

    def get(self, request, *args, **kwargs):
        if request.session["previous_view"] is None:
            return HttpResponseForbidden()
        request.session["previous_view"] = None
        return super().get(request, *args, **kwargs)