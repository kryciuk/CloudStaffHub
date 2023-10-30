from django.views.generic import CreateView

from recruiter.forms import PositionsForm
from organizations.models import Department


class PositionCreateView(CreateView):

    form_class = PositionsForm
    template_name = "recruiter/positions_create.html"
    context_object_name = "position"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"].fields["department"].queryset = Department.objects.filter(company=self.request.user.profile.company)
        return context

    def form_valid(self, form):
        form.instance.company = self.request.user.profile.company
        return super().form_valid(form)
