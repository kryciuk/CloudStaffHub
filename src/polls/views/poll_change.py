from django.views.generic import UpdateView

from polls.models import Poll


class PollUpdateView(UpdateView):
    model = Poll
    context_object_name = "poll"
    template_name = "polls/poll_detail.html"
