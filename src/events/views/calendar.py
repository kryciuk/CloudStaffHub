import calendar
from calendar import HTMLCalendar
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView
from events.models import Assignment


class CalendarDetailView(LoginRequiredMixin, TemplateView):
    template_name = "events/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        year, month_number = kwargs.get('year'), kwargs.get('month_number')
        month_name = calendar.month_name[month_number]

        cal = HTMLCalendar().formatmonth(year, month_number)

        context['year'] = year
        context['previous_year'] = year-1
        context['next_year'] = year + 1

        context['previous_month'] = month_number - 1
        context['next_month'] = month_number + 1

        context['month_name'] = month_name
        context['month_number'] = month_number
        context['username'] = self.request.user.first_name
        context['cal'] = cal

        assignments = Assignment.objects.filter(event_date__year=year, event_date__month=month_number, employee=self.request.user, status=False).order_by('event_date')
        context['assignments'] = assignments

        return context

