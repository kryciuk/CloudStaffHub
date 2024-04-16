import datetime
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from funcy import join_with

from core.base import redirect_to_dashboard_based_on_group
from polls.forms import PollCloseForm
from polls.models import Poll, PollAnswer, PollResults


class PollCloseView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Poll
    permission_required = "polls.change_poll"
    context_object_name = "poll"
    success_url = reverse_lazy("poll-list")
    form_class = PollCloseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Poll Close - CloudStaffHub"
        return context

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def post(self, request, *args, **kwargs):
        poll_id = kwargs["pk"]
        all_poll_answers = PollAnswer.objects.filter(poll=poll_id)
        pool_results = self.__clean_answers(all_poll_answers)
        if pool_results:
            poll_final_results = PollResults(poll_id=poll_id, results=pool_results, close_date=datetime.datetime.now())
            poll_final_results.save()
        return super().post(request, *args, **kwargs)

    def __clean_answers(self, all_answers):
        list_results = []
        for answer in all_answers:
            results = json.loads(answer.result)
            list_results.append(results)
        merged_dict = join_with(tuple, list_results)
        if merged_dict:
            merged_dict.pop("csrfmiddlewaretoken")
        return merged_dict

    def form_valid(self, form):
        form.instance.status = False
        messages.success(self.request, "Poll successfully closed.")
        return super().form_valid(form)
