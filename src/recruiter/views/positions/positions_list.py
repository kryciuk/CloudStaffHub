from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView

from organizations.models import Position
from recruiter.filters import PositionFilter


class PositionListView(UserPassesTestMixin, ListView):
    template_name = "recruiter/positions_list.html"
    context_object_name = "positions"
    queryset = Position.objects.all()

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.groups.filter(name="Recruiter").exists() or
            self.request.user.groups.filter(name="Manager").exists()
            or self.request.user.groups.filter(name="Owner").exists()
            or self.request.user.is_superuser)

    def get_queryset(self):
        queryset = Position.objects.filter(company=self.request.user.profile.company).all()
        self.filterset = PositionFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filterset.form
        return context
