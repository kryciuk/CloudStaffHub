from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from organizations.models import Position


class PositionDeleteView(UserPassesTestMixin, DeleteView):
    model = Position
    template_name = "recruiter/positions_delete.html"
    context_object_name = "positions"
    success_url = reverse_lazy("positions-list")

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.groups.filter(name="Recruiter").exists() or
            self.request.user.groups.filter(name="Manager").exists()
            or self.request.user.groups.filter(name="Owner").exists()
            or self.request.user.is_superuser)