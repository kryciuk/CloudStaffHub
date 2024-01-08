from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from core.base import has_group
from polls.models import Poll


class PollListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Poll
    permission_required = "polls.add_poll"
    context_object_name = "polls"
    template_name = "polls/poll_list.html"
    queryset = Poll.objects.all()

    def handle_no_permission(self):
        messages.warning(self.request, "You don't have the required permissions to create a poll.")
        if has_group(self.request.user, "Candidate"):
            return HttpResponseRedirect(reverse("dashboard-candidate"))
        return HttpResponseRedirect(reverse("dashboard-employee"))

    def get_queryset(self):
        queryset = super().get_queryset().filter(questionnaire__company=self.request.user.profile.company)
        queryset = queryset.order_by("-status", "-date_created")
        return queryset
