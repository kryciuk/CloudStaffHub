import json

from django.urls import reverse
from django.views.generic import UpdateView

from evaluation.forms import EvaluationUpdateForm
from evaluation.models import Evaluation


class EvaluationUpdateView(UpdateView):
    model = Evaluation
    form_class = EvaluationUpdateForm
    template_name = "evaluation/evaluation_update.html"
    context_object_name = "evaluation"

    def form_valid(self, form):
        result = json.dumps(self.request._post)
        form.instance.result = result
        form.instance.status = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("evaluation-complete", kwargs={"pk": self.object.pk})
