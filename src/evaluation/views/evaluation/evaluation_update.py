import json

from django.urls import reverse
from django.views.generic import UpdateView

from evaluation.forms import EvaluationUpdateEmployeeForm, EvaluationUpdateManagerForm
from evaluation.models import Evaluation


class EvaluationUpdateEmployeeView(UpdateView):
    model = Evaluation
    form_class = EvaluationUpdateEmployeeForm
    template_name = "evaluation/evaluation/evaluation_update.html"
    context_object_name = "evaluation"

    def form_valid(self, form):
        result = json.dumps(self.request._post)
        form.instance.result_employee = result
        form.instance.status_employee = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dashboard-employee")


class EvaluationUpdateManagerView(UpdateView):
    model = Evaluation
    form_class = EvaluationUpdateManagerForm
    template_name = "evaluation/evaluation/evaluation_update.html"
    context_object_name = "evaluation"

    def form_valid(self, form):
        result = json.dumps(self.request._post)
        form.instance.result_manager = result
        form.instance.status_manager = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dashboard-manager")
