from itertools import chain

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView

from core.base import redirect_to_dashboard_based_on_group
from evaluation.models import Answer
from polls.models import PollResults


class PollResultsView(UserPassesTestMixin, DetailView):
    model = PollResults
    template_name = "polls/poll_results.html"
    context_object_name = "poll_results"

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def test_func(self):
        poll_results = self.get_object()
        user_groups = ["Employee", "Recruiter", "Manager", "Owner"]
        return (
            self.request.user.is_superuser
            or self.request.user.is_authenticated
            and (self.request.user.profile.company == poll_results.poll.questionnaire.company)
            and (self.request.user.groups.filter(name__in=user_groups).exists())
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = context["poll_results"]
        final_results = {}
        for question, answers in results.results.items():
            final_results[question] = [Answer.objects.get(id=int(id_)) for id_ in answers]

        questionnaire = results.poll.questionnaire
        questions = questionnaire.questions.all()
        display_results = {}
        most_picked = []

        for question in questions:
            count_answers = {}
            result_per_question = final_results[question.text]
            for answer in question.answers.all():
                count_answers[answer] = result_per_question.count(answer)
                display_results[question] = count_answers
            max_value = max(count_answers.values())
            most_picked_per_question = [key for key, value in count_answers.items() if value == max_value]
            most_picked.append(most_picked_per_question)

        context["display_results"] = display_results
        context["most_picked"] = list(chain(*most_picked))
        context["title"] = "Poll Results - CloudStaffHub"
        return context
