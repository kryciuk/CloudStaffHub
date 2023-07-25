# from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView

from evaluation.forms import QuestionForm


class QuestionCreate(CreateView):          # PermissionRequiredMixin
    # permission_required = "recruitment.add_joboffer"

    form_class = QuestionForm
    template_name = "evaluation/question_create.html"
    context_object_name = "question"
