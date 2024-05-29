from django.views.generic import DetailView

from evaluation.forms import EvaluationCreateForm
from evaluation.models import Evaluation


class EvaluationDetailView(DetailView):
    model = Evaluation
    form_class = EvaluationCreateForm
    template_name = "evaluation/evaluation/evaluation_detail.html"
    context_object_name = "evaluation"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context
