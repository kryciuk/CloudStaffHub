from django.shortcuts import reverse
from django.views.generic import CreateView

from evaluation.forms import QuestionnaireForm


class QuestionnaireCreateView(CreateView):
    form_class = QuestionnaireForm
    context_object_name = "questionnaire"
    template_name = "evaluation/questionnaire_create.html"

    def form_valid(self, form):
        form.instance.company = self.request.user.profile.company
        form.instance.created_by = self.request.user
        form.instance.status = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("question-create", kwargs={"id_questionnaire": self.object.id})
