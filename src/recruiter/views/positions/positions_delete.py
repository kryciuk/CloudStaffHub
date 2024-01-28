from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from organizations.models import Position


class PositionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Position
    context_object_name = "positions"
    success_url = reverse_lazy("positions-list")
    permission_required = "organizations.delete_position"
