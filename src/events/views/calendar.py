import calendar
from calendar import HTMLCalendar

from django.views.generic import TemplateView


class CalendarDetailView(TemplateView):
    template_name = "events/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        year, month = kwargs.get('year'), kwargs.get('month').capitalize()
        month_number = int(list(calendar.month_name).index(month))

        cal = HTMLCalendar().formatmonth(year, month_number)

        context['year'] = year
        context['month'] = month
        context['user'] = self.request.user.first_name
        context['cal'] = cal
        return context

