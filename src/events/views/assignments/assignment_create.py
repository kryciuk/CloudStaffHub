import calendar
import datetime

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.views.generic import CreateView

from core.base import has_group
from events.forms import AssigmentForm


class AssignmentCreateView(CreateView):
    form_class = AssigmentForm
    template_name = "events/assignments/assignment_create.html"
    context_object_name = "assignment"

    def form_valid(self, form):
        if has_group(self.request.user, "Manager") or has_group(self.request.user, "Creator"):
            form.instance.manager = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"].fields["employee"].queryset = User.objects.filter(profile__company=self.request.user.profile.company).all()
        return context

    def get_success_url(self):
        year, month_number = datetime.datetime.now().year, datetime.datetime.now().month
        month = list(calendar.month_name)[month_number]
        return reverse('calendar', args=(year, month))
