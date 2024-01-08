from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils import timezone
from django.views.generic import CreateView

from core.base import has_group
from evaluation.models import Questionnaire
from polls.forms import PollCreateForm
from polls.models import Poll


class PollCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Poll
    form_class = PollCreateForm
    permission_required = "polls.add_poll"
    template_name = "polls/poll_create.html"
    context_object_name = "poll"

    def handle_no_permission(self):
        messages.warning(self.request, "You don't have the required permissions to create a poll.")
        if has_group(self.request.user, "Candidate"):
            return HttpResponseRedirect(reverse("dashboard-candidate"))
        return HttpResponseRedirect(reverse("dashboard-employee"))

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["questionnaire"].queryset = Questionnaire.objects.filter(
            company=self.request.user.profile.company
        ).filter(type=Questionnaire.Type.POLL)
        return form

    def form_valid(self, form):
        form.instance.status = True
        form.instance.date_created = timezone.now()
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dashboard-manager")
