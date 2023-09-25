from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import reverse

from polls.models import Poll
from polls.forms import PollUpdateForm


class PollCloseView(UpdateView):
    model = Poll
    context_object_name = "poll"
    success_url = reverse_lazy("poll-list")
    form_class = PollUpdateForm

    def form_valid(self, form):
        form.instance.status = False
        return super().form_valid(form)
