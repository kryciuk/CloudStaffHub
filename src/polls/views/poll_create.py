from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import reverse
from django.utils import timezone
from django.views.generic import CreateView

from core.base import redirect_to_dashboard_based_on_group
from evaluation.models import Questionnaire
from polls.forms import PollCreateForm
from polls.models import Poll


class PollCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Poll
    form_class = PollCreateForm
    permission_required = "polls.add_poll"
    template_name = "polls/poll_create.html"
    context_object_name = "poll"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Poll Create - CloudStaffHub"
        return context

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

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
        messages.success(self.request, "Poll successfully created.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dashboard-manager")
