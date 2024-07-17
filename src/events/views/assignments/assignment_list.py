from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.views.generic import ListView

from core.base import redirect_to_dashboard_based_on_group
from events.models import Assignment


class AssignmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "events/assignments/assignment_list.html"
    permission_required = "events.add_assignment"

    def get_queryset(self, **kwargs):
        queryset = Assignment.objects.filter(employee=self.request.user, status=False).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        year = timezone.now().year
        month = timezone.now().month
        context["year"] = year
        context["month"] = month

        context["title"] = "Assignment List - CloudStaffHub"

        return context

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")
