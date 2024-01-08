import json

from django.contrib import messages
from django.shortcuts import reverse
from django.utils import timezone
from django.views.generic import RedirectView

from polls.models import Poll, PollAnswer


class PollAnswerView(RedirectView):
    model = PollAnswer
    context_object_name = "poll"

    def post(self, request, *args, **kwargs):
        poll_id = kwargs["pk"]
        results = json.dumps(self.request.POST)
        poll = Poll.objects.get(id=poll_id)
        PollAnswer.objects.create(respondent=self.request.user, date_filled=timezone.now(), poll=poll, result=results)
        messages.success(request, "Your answer was successfully saved.")
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        group = self.request.user.groups.first()
        match group.name:
            case "Candidate":
                return reverse("dashboard-candidate")
            case "Recruiter":
                return reverse("dashboard-recruiter")
            case "Manager":
                return reverse("dashboard-manager")
            case "Owner":
                return reverse("dashboard-owner")
            case _:
                return reverse("dashboard-employee")
