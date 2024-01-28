import json

from django.contrib import messages
from django.shortcuts import reverse
from django.utils import timezone
from django.views.generic import RedirectView

from core.consts import GROUPS
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
            case GROUPS.GROUP__OWNER:
                return reverse("dashboard-owner")
            case GROUPS.GROUP__EMPLOYEE:
                return reverse("dashboard-employee")
            case GROUPS.GROUP__MANAGER:
                return reverse("dashboard-manager")
            case GROUPS.GROUP__CANDIDATE:
                return reverse("dashboard-candidate")
            case GROUPS.GROUP__RECRUITER:
                return reverse("dashboard-recruiter")
            case _:
                return reverse("dashboard-employee")
