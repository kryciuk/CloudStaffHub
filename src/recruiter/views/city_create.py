from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.views.generic import CreateView

from recruiter.forms import CityForm


class CityCreateView(UserPassesTestMixin, CreateView):

    form_class = CityForm
    template_name = "recruiter/city_create.html"
    context_object_name = "city"

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.groups.filter(name="Recruiter").exists() or
            self.request.user.groups.filter(name="Manager").exists()
            or self.request.user.groups.filter(name="Owner").exists()
            or self.request.user.is_superuser)

    def get_success_url(self):
        if self.request.session.get("previous_view") == "JobOffersCreateView":
            self.request.session["previous_view"] = None
            return reverse("job-offer-create")
        return reverse("dashboard-recruiter")
