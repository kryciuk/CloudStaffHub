from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView

from recruiter.forms import CityForm


class CityCreate(PermissionRequiredMixin, CreateView):
    permission_required = "recruiter"

    form_class = CityForm
    template_name = "recruiter/city_create.html"
    context_object_name = "city"
