import json
from datetime import datetime

from django.contrib import messages
from django.shortcuts import reverse
from django.views.generic import RedirectView

from polls.models import Poll, PollAnswer


class PollAnswerView(RedirectView):
    model = PollAnswer
    context_object_name = "poll"

    def get(self, request, *args, **kwargs):
        poll_id = kwargs['pk']
        results = json.dumps(self.request._post)
        poll = Poll.objects.get(id=poll_id)
        new_answer = PollAnswer(respondent=self.request.user, date_filled=datetime.now(), poll=poll, result=results)
        new_answer.save()
        messages.success(request, f"Your answer was successfully saved")
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse("dashboard-employee")
