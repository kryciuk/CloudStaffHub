from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from events.forms import AssignmentStatusForm
from events.models import Assignment


class AssignmentCloseView(UpdateView):
    model = Assignment
    form_class = AssignmentStatusForm
    context_object_name = "assignment"
    success_url = reverse_lazy("assignments")

    def form_valid(self, form):
        form.instance.status = True
        messages.success(self.request, "Assignment is now closed.")
        return super().form_valid(form)
