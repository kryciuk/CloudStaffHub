from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import reverse

from events.forms import AssigmentStatusForm
from events.models import Assignment


class AssignmentCloseView(UpdateView):
    model = Assignment
    form_class = AssigmentStatusForm
    context_object_name = "assignment"
    success_url = reverse_lazy("assignments")

    def form_valid(self, form):
        form.instance.status = True
        return super().form_valid(form)
