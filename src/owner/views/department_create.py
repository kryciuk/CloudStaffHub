from django.views.generic import CreateView
from django.shortcuts import reverse

from owner.forms import DepartmentForm


class DepartmentCreateView(CreateView):
    form_class = DepartmentForm
    template_name = "owner/department_create.html"
    context_object_name = "department"

    def form_valid(self, form):
        form.instance.company = self.request.user.profile.company
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dashboard-owner')