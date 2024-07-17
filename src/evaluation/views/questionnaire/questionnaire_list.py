from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView

from evaluation.filters import QuestionnaireFilter
from evaluation.models import Questionnaire


class QuestionnaireListByUserView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Questionnaire
    context_object_name = "questionnaires"
    template_name = "evaluation/questionnaire/questionnaire_list.html"
    queryset = Questionnaire.objects.all()
    permission_required = "evaluation.add_questionnaire"

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(company=self.request.user.profile.company, status=True)
        self.filterset = QuestionnaireFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = self.filterset.form
        context["title"] = "Questionnaire List - CloudStaffHub"
        return context
