import datetime
import json

from funcy import join_with
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import reverse

from polls.models import Poll, PollAnswer, PollResults
from polls.forms import PollUpdateForm


class PollCloseView(UpdateView):
    model = Poll
    context_object_name = "poll"
    success_url = reverse_lazy("poll-list")
    form_class = PollUpdateForm

    def post(self, request, *args, **kwargs):
        poll_id = kwargs['pk']
        all_poll_answers = PollAnswer.objects.filter(poll=poll_id).all()
        list_results = []
        for answer in all_poll_answers:
            results = json.loads(answer.result)
            list_results.append(results)
        merged_dict = join_with(tuple, list_results)
        merged_dict.pop('csrfmiddlewaretoken')
        poll_final_results = PollResults(poll_id=poll_id, results=merged_dict, close_date=datetime.datetime.now())
        poll_final_results.save()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.status = False
        return super().form_valid(form)
