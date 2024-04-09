from django.views.generic import UpdateView

from evaluation.models import Questionnaire


class QuestionnaireUpdateView(UpdateView):
    model = Questionnaire
    template_name = "evaluation/questionnaire_update.html"
    fields = "__all__"
