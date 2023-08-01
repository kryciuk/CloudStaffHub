from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView

from recruiter.forms import PositionForm


class PositionCreate(PermissionRequiredMixin, CreateView):
    permission_required = "recruiter"

    form_class = PositionForm
    template_name = "recruiter/position_create.html"
    context_object_name = "position"
