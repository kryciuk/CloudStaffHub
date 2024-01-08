from itertools import chain

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView

from evaluation.models import Questionnaire
from polls.models import Poll, PollAnswer


class PollFillView(UserPassesTestMixin, DetailView):
    model = Poll
    context_object_name = "poll"
    template_name = "polls/poll_fill.html"

    def handle_no_permission(self):
        messages.warning(
            self.request,
            "You cannot view this poll. It appears you've either already completed it, "
            "lack the necessary permissions or this poll is already closed.",
        )
        group = self.request.user.groups.first()
        match group.name:
            case "Candidate":
                return HttpResponseRedirect(reverse("dashboard-candidate"))
            case "Recruiter":
                return HttpResponseRedirect(reverse("dashboard-recruiter"))
            case "Manager":
                return HttpResponseRedirect(reverse("dashboard-manager"))
            case "Owner":
                return HttpResponseRedirect(reverse("dashboard-owner"))
            case _:
                return HttpResponseRedirect(reverse("dashboard-employee"))

    def test_func(self):
        poll = self.get_object()
        user_groups = ["Employee", "Recruiter", "Manager", "Owner"]
        poll_answer_user_check = PollAnswer.objects.filter(poll=poll, respondent=self.request.user)
        return (
            self.request.user.is_superuser
            or self.request.user.is_authenticated
            and (self.request.user.profile.company == poll.questionnaire.company)
            and (self.request.user.groups.filter(name__in=user_groups).exists())
            and not poll_answer_user_check
            and poll.status
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionnaire = Questionnaire.objects.get(id=self.object.questionnaire.id)
        questions = questionnaire.questions.all()
        answers = {}
        for question in questions:
            answers[question] = list(chain(question.answers.all()))
        context["questions"] = questions
        context["answers"] = answers
        context["poll_id"] = self.object.id
        return context
