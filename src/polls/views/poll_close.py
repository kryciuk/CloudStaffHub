import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from funcy import join_with

from polls.forms import PollCloseForm
from polls.models import Poll, PollAnswer, PollResults


class PollCloseView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Poll
    permission_required = "polls.change_poll"
    context_object_name = "poll"
    success_url = reverse_lazy("poll-list")
    form_class = PollCloseForm

    def post(self, request, *args, **kwargs):
        poll_id = kwargs["pk"]
        all_poll_answers = PollAnswer.objects.filter(poll=poll_id)
        pool_results = self.__clean_answers(all_poll_answers)
        poll_final_results = PollResults(poll_id=poll_id, results=pool_results, close_date=datetime.datetime.now())
        poll_final_results.save()
        return super().post(request, *args, **kwargs)

    def __clean_answers(self, all_answers):
        list_results = []
        for answer in all_answers:
            results = json.loads(answer.result)
            list_results.append(results)
        merged_dict = join_with(tuple, list_results)
        merged_dict.pop("csrfmiddlewaretoken")
        return merged_dict

    def form_valid(self, form):
        form.instance.status = False
        return super().form_valid(form)
