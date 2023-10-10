from django.views.generic import ListView

from events.models import Assignment


class AssignmentListView(ListView):
    model = Assignment
    context_object_name = "assigment"
    template_name = "events/assignments/assignment_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        assignment_for_user = Assignment.objects.filter(employee=self.request.user).distinct()
        context['assignment_for_user'] = assignment_for_user
        return context
