from django.views.generic import ListView

from evaluation.models import Questionnaire


class QuestionnaireListByUserView(ListView):
    model = Questionnaire
    context_object_name = "questionnaires"
    template_name = "evaluation/questionnaire_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["questionnaires_evaluation"] = Questionnaire.objects.filter(created_by=self.request.user).filter(
            type=Questionnaire.Type.EVALUATION
        )
        context["questionnaires_polls"] = Questionnaire.objects.filter(created_by=self.request.user).filter(
            type=Questionnaire.Type.POLL
        )
        return context
