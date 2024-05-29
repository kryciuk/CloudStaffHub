from itertools import chain

from django.views.generic import DetailView

from evaluation.models import Evaluation, Questionnaire


class QuestionnaireFillView(DetailView):
    model = Questionnaire
    context_object_name = "questionnaire"
    template_name = "evaluation/questionnaire/questionnaire_fill.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionnaire = Questionnaire.objects.get(id=self.object.id)
        questions = questionnaire.questions.all()
        answers = {}
        for question in questions:
            answers[question] = list(chain(question.answers.all()))
        context["questions"] = questions
        context["answers"] = answers
        context["id_evaluation"] = self.kwargs.get("id_evaluation")
        evaluation = Evaluation.objects.get(id=self.kwargs.get("id_evaluation"))
        if evaluation.manager.username == self.request.user.username:
            context["is_manager"] = "yes"
        else:
            context["is_manager"] = "no"
        return context

    # def get_success_url(self):
    #     return redirect("evaluation-detail", args=["id_evaluation"])
