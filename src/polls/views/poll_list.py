from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView
from core.base import redirect_to_dashboard_based_on_group
from polls.models import Poll


class PollListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Poll
    permission_required = "polls.add_poll"
    context_object_name = "polls"
    template_name = "polls/poll_list.html"
    queryset = Poll.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Poll List - CloudStaffHub"
        return context

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def get_queryset(self):
        queryset = super().get_queryset().filter(questionnaire__company=self.request.user.profile.company)
        queryset = queryset.order_by("-status", "-date_created")
        return queryset
