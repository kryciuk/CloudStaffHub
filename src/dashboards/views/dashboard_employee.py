import calendar
from datetime import date, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from evaluation.models import Evaluation
from polls.models import Poll, PollResults


class UserHasEmployeeOrHigherGroup(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.groups.filter(name="Employee").exists()
            or self.request.user.groups.filter(name="Manager").exists()
            or self.request.user.groups.filter(name="Recruiter").exists()
            or self.request.user.groups.filter(name="Creator").exists()
        )


class EmployeeDashboardView(UserHasEmployeeOrHigherGroup, TemplateView):
    template_name = "dashboards/dashboard_employee.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # evaluations

        assigned_evaluations = Evaluation.objects.filter(
            employee=self.request.user, status=False
        ).order_by("-date_end")[:5]
        completed_evaluations = Evaluation.objects.filter(
            employee=self.request.user, status=True
        )
        context["assigned_evaluations"] = assigned_evaluations
        context["completed_evaluations"] = completed_evaluations

        # polls

        open_polls = Poll.objects.filter(status=True, questionnaire__company=self.request.user.profile.company)
        for poll in open_polls:
            answers = poll.answers.all()
            for answer in answers:
                if answer.respondent == self.request.user:
                    open_polls = open_polls.exclude(id=poll.id)
        context["open_polls"] = open_polls

        today = date.today()
        poll_results = PollResults.objects.filter(poll__questionnaire__company=self.request.user.profile.company, close_date__lte=today + timedelta(7))
        context["poll_results"] = poll_results

        # calendar, events

        year = date.today().year
        month_number = date.today().month
        month_name = list(calendar.month_name)[month_number]

        context["year"] = year
        context["month_number"] = month_number
        context["month_name"] = month_name

        return context
