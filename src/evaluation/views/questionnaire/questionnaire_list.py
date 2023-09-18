from django.views.generic import ListView

from evaluation.models import Questionnaire


class QuestionnaireListView(ListView):
    model = Questionnaire
    context_object_name = "questionnaires"

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(*, object_list=None, **kwargs)
