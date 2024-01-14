from itertools import chain

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import DetailView

from core.base import redirect_to_dashboard_based_on_group
from evaluation.models import Questionnaire
from polls.models import Poll, PollAnswer


class PollFillView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DetailView):
    model = Poll
    context_object_name = "poll"
    permission_required = ["Poll.view_poll"]
    template_name = "polls/poll_fill.html"

    def handle_no_permission(self):
        messages.warning(
            self.request,
            "You cannot view this poll. It appears you've either already completed it, "
            "lack the necessary permissions or this poll is already closed.",
        )
        group = self.request.user.groups.first()
        return redirect_to_dashboard_based_on_group(group.name)

    def test_func(self):
        poll = self.get_object()
        # user_groups = ["Employee", "Recruiter", "Manager", "Owner"]
        poll_answer_user_check = PollAnswer.objects.filter(poll=poll, respondent=self.request.user)
        return self.request.user.is_superuser or (
            # or (self.request.user.is_authenticated
            (self.request.user.profile.company == poll.questionnaire.company)
            # and (self.request.user.groups.filter(name__in=user_groups).exists())
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
