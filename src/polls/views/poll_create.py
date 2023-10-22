from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.views.generic import CreateView

from evaluation.models import Questionnaire
from polls.forms import PollCreateForm
from polls.models import Poll


class PollCreateView(CreateView):
    model = Poll
    form_class = PollCreateForm
    template_name = "polls/poll_create.html"
    context_object_name = "poll"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["questionnaire"].queryset = Questionnaire.objects.filter(
            created_by=self.request.user).filter(type=Questionnaire.Type.POLL)
        return form

    def form_valid(self, form):
        form.instance.status = True
        form.instance.date_created = datetime.now()
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dashboard-manager")
