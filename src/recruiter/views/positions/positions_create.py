from django.views.generic import CreateView

from recruiter.forms import PositionsForm


class PositionCreateView(CreateView):

    form_class = PositionsForm
    template_name = "recruiter/positions_create.html"
    context_object_name = "position"

    def form_valid(self, form):
        form.instance.company = self.request.user.profile.company
        return super().form_valid(form)