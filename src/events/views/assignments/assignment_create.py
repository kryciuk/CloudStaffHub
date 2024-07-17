import datetime

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils import timezone
from django.views.generic import CreateView

from core.base import has_group, redirect_to_dashboard_based_on_group
from events.forms import AssignmentForm


class AssignmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = AssignmentForm
    template_name = "events/assignments/assignment_create.html"
    context_object_name = "assignment"
    permission_required = "events.add_assignment"

    def get_form(self, form_class=AssignmentForm):
        form = super().get_form()
        form.fields["event_date"].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        if has_group(self.request.user, "Manager") or has_group(self.request.user, "Owner"):
            form.instance.manager = self.request.user
        messages.success(self.request, "New assignment has been added.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"].fields["employee"].queryset = User.objects.filter(
            profile__company=self.request.user.profile.company
        ).all()
        year = timezone.now().year
        month = timezone.now().month
        context["year"] = year
        context["month"] = month

        context["title"] = "Create Assignment - CloudStaffHub"

        return context

    def get_success_url(self):
        year, month_number = datetime.datetime.now().year, datetime.datetime.now().month
        return reverse("calendar", args=(year, month_number))

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")
