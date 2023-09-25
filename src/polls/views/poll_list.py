from django.views.generic import ListView

from polls.models import Poll


class PollListView(ListView):
    model = Poll
    context_object_name = "polls"
    template_name = "polls/poll_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["polls"] = Poll.objects.filter(questionnaire__company=self.request.user.profile.company)
        return context
