import calendar
from datetime import date, timedelta

import requests
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

from core.base import redirect_to_dashboard_based_on_group
from evaluation.models import Evaluation
from polls.models import Poll, PollResults


class EmployeeDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboards/dashboard_employee.html"

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You don't have the required permissions to access this page.")
            group = self.request.user.groups.first()
            return redirect_to_dashboard_based_on_group(group.name)
        messages.warning(self.request, "You are not logged in.")
        return redirect_to_dashboard_based_on_group("")

    def test_func(self):
        groups = ["Employee", "Recruiter", "Manager", "Owner"]
        return self.request.user.is_authenticated and (self.request.user.groups.filter(name__in=groups).exists())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # evaluations

        assigned_evaluations = Evaluation.objects.filter(employee=self.request.user, status_employee=False).order_by(
            "-date_end"
        )[:5]
        completed_evaluations = Evaluation.objects.filter(
            employee=self.request.user, status_employee=True, status_manager=True
        )
        context["assigned_evaluations"] = assigned_evaluations
        context["completed_evaluations"] = completed_evaluations

        # polls

        open_polls = Poll.objects.prefetch_related("answers").filter(
            status=True, questionnaire__company=self.request.user.profile.company
        )
        for poll in open_polls:
            answers = poll.answers.all()
            for answer in answers:
                if answer.respondent == self.request.user:
                    open_polls = open_polls.exclude(id=poll.id)
        context["open_polls"] = open_polls

        today = date.today()
        poll_results = PollResults.objects.select_related("poll").filter(
            poll__questionnaire__company=self.request.user.profile.company, close_date__lte=today + timedelta(7)
        )
        context["poll_results"] = poll_results

        # calendar, events

        year = date.today().year
        month_number = date.today().month
        month_name = list(calendar.month_name)[month_number]

        context["year"] = year
        context["month_number"] = month_number
        context["month_name"] = month_name

        # weather

        results = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?lat=52.2319581&lon=21.0067249&units=metric&appid"
            "=f539c944fc495f7a160041b0d2bd8f21",
            timeout=5,
        ).json()
        context["weather"] = results

        context["title"] = "Employee's Dashboard - CloudStaffHub"

        return context
