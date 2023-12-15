from django.views.generic import ListView

from polls.models import Poll


class PollListView(ListView):
    model = Poll
    context_object_name = "polls"
    template_name = "polls/poll_list.html"
    queryset = Poll.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(questionnaire__company=self.request.user.profile.company)
