from django.utils import timezone
from django.views.generic import ListView

from events.models import Assignment


class AssignmentListView(ListView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "events/assignments/assignment_list.html"

    def get_queryset(self, **kwargs):
        queryset = Assignment.objects.filter(employee=self.request.user, status=False).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        year = timezone.now().year
        month = timezone.now().month
        context["year"] = year
        context["month"] = month
        return context
