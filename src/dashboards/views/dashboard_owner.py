from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.views.generic import TemplateView


class UserHasCreatorGroup(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(
            Q(name='Creator') | Q(name='Manager')).exists()


class OwnerDashboardView(UserHasCreatorGroup, TemplateView):
    template_name = "dashboards/dashboard_owner.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.user.profile.company
        context["employees"] = User.objects.filter(profile__company=company).order_by('-id')[:10]
        return context
