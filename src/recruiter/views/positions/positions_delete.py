from django.urls import reverse_lazy
from django.views.generic import DeleteView

from organizations.models import Position


class PositionDeleteView(DeleteView):
    model = Position
    template_name = "recruiter/positions_delete.html"
    context_object_name = "positions"
    success_url = reverse_lazy("positions-list")
