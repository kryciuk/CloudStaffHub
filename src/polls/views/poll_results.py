from collections import Counter
from itertools import chain

from django.views.generic import DetailView

from evaluation.models import Answer
from polls.models import PollResults


class PollResultsView(DetailView):
    model = PollResults
    template_name = "polls/poll_results.html"
    context_object_name = "poll_results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = context["poll_results"]
        final_results = {}
        for question, answers in results.results.items():
            final_results[question] = [Answer.objects.get(id=int(id_)) for id_ in answers]

        questionnaire = results.poll.questionnaire
        questions = questionnaire.questions.all()
        display_results = {}
        most_picked = []

        for question in questions:
            count_answers = {}
            result_per_question = final_results[question.text]
            for answer in question.answers.all():
                count_answers[answer] = result_per_question.count(answer)
                display_results[question] = count_answers
            max_value = max(count_answers.values())
            most_picked_per_question = [key for key, value in count_answers.items() if value == max_value]
            most_picked.append(most_picked_per_question)

        context["display_results"] = display_results
        context["most_picked"] = list(chain(*most_picked))
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     results = context['poll_results']
    #     questionnaire = results.poll.questionnaire
    #     questions = questionnaire.questions.all()
    #     display_results = {}
    #     most_picked = {}
    #     for question in questions:
    #         result_per_question = results.results[question.text]
    #         count_answers = {}
    #         for answer in question.answers.all():
    #             count_answers[answer.answer] = result_per_question.count(answer.answer)
    #         display_results[question.text] = count_answers
    #         max_value = max(count_answers.values())
    #         most_picked_answers = [key for key, value in count_answers.items() if value == max_value]
    #         most_picked[question] = most_picked_answers
    #     context['display_results'] = display_results
    #     context['most_picked'] = sum(most_picked.values(), [])
    #     return context

    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     results = context['poll_results']
    #     final_results = {}
    #     for question, answers in results.results.items():
    #         final_results[question] = [Answer.objects.get(id=int(id)) for id in answers]
    #
    #     questionnaire = results.poll.questionnaire
    #     questions = questionnaire.questions.all()
    #     display_results = {}
    #     most_picked = []
    #
    #     for question in questions:
    #         count_answers = {}
    #         result_per_question = results.results[question.text]
    #         for answer in question.answers.all():
    #             count_answers[answer] = result_per_question.count(answer)
    #             display_results[question] = count_answers
    #         most_picked_per_question = list(set(final_results[question.text]))
    #         most_picked.append(most_picked_per_question)
    #
    #     context['display_results'] = display_results
    #     context['most_picked'] = most_picked
    #     return context
