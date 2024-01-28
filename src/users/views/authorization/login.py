from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from core.consts import GROUPS


class UserLoginView(LoginView):
    template_name = "users/authorization/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login - CloudStaffHub"
        return context

    def form_invalid(self, form):
        messages.warning(self.request, "Your login details are incorrect.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Logged in successfully. Welcome to CloudStaffHub.")
        return super().form_valid(form)

    def get_success_url(self):
        group = self.request.user.groups.first()
        match group.name:
            case GROUPS.GROUP__OWNER:
                return reverse_lazy("dashboard-owner")
            case GROUPS.GROUP__EMPLOYEE:
                return reverse_lazy("dashboard-employee")
            case GROUPS.GROUP__MANAGER:
                return reverse_lazy("dashboard-manager")
            case GROUPS.GROUP__CANDIDATE:
                return reverse_lazy("dashboard-candidate")
            case GROUPS.GROUP__RECRUITER:
                return reverse_lazy("dashboard-recruiter")
            case _:
                return reverse_lazy("dashboard-employee")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            group = self.request.user.groups.first()
            match group.name:
                case GROUPS.GROUP__OWNER:
                    return redirect("dashboard-owner")
                case GROUPS.GROUP__EMPLOYEE:
                    return redirect("dashboard-employee")
                case GROUPS.GROUP__MANAGER:
                    return redirect("dashboard-manager")
                case GROUPS.GROUP__CANDIDATE:
                    return redirect("dashboard-candidate")
                case GROUPS.GROUP__RECRUITER:
                    return redirect("dashboard-recruiter")
                case _:
                    return redirect("dashboard-employee")
        return super().get(request, *args, **kwargs)
