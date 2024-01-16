import json

from django.test import TransactionTestCase, tag
from django.urls import reverse
from rest_framework import status

from evaluation.factories import AnswerFactory, QuestionFactory, QuestionnaireFactory
from evaluation.models import Questionnaire
from polls.factories import PollFactory
from polls.models import Poll, PollAnswer, PollResults
from users.factories import CandidateFactory, EmployeeFactory, OwnerFactory


class TestPollCreateView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.questionnaire = QuestionnaireFactory.create(
            company=self.user_owner.profile.company, type=Questionnaire.Type.POLL
        )
        self.question = QuestionFactory.create(questionnaire=self.questionnaire)
        self.answers = AnswerFactory.create_batch(5, question=self.question)

    def test_if_candidate_cant_access_view_and_is_redirected_to_correct_dashboard(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("poll-create"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("dashboard-candidate"))

    def test_if_regular_employee_cant_access_view_and_is_redirected_to_correct_dashboard(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("poll-create"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("dashboard-employee"))

    def test_if_message_is_shown_if_access_to_view_is_denied(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("poll-create"), follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.message, "You don't have the required permissions to create a poll.")

    def test_if_owner_can_access_view(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("poll-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_owner_can_create_poll(self):
        self.client.force_login(self.user_owner)
        response = self.client.post(
            reverse("poll-create"), data={"questionnaire": self.questionnaire.id, "date_end": "2030-10-10"}
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Poll.objects.count(), 1)

    def test_if_employee_cant_create_poll(self):
        self.client.force_login(self.user_employee)
        response = self.client.post(
            reverse("poll-create"), data={"questionnaire": self.questionnaire.id, "date_end": "2030-10-10"}
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Poll.objects.count(), 0)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("poll-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "polls/poll_create.html")


@tag("x")
class TestPollFillView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner1 = OwnerFactory.create()
        self.user_owner2 = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_employee.profile.company = self.user_owner1.profile.company
        self.user_employee.profile.save()
        self.user_candidate = CandidateFactory.create()
        self.questionnaire = QuestionnaireFactory.create(
            company=self.user_owner1.profile.company, type=Questionnaire.Type.POLL
        )
        self.question = QuestionFactory.create(questionnaire=self.questionnaire)
        self.answers = AnswerFactory.create_batch(5, question=self.question)
        self.poll = PollFactory.create(questionnaire=self.questionnaire)

    def test_if_candidate_cant_access_view_and_is_redirected_to_correct_dashboard(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("poll-fill", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("dashboard-candidate"))

    def test_if_employee_can_access_view_if_correct_company(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("poll-fill", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_user_cant_access_view_if_incorrect_company(self):
        self.client.force_login(self.user_owner2)
        response = self.client.get(reverse("poll-fill", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_user_cant_access_view_if_poll_answer_was_submitted(self):
        self.client.force_login(self.user_employee)
        PollAnswer.objects.create(respondent=self.user_employee, date_filled="2030-10-10", poll=self.poll, result={})
        response = self.client.get(reverse("poll-fill", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("poll-fill", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "polls/poll_fill.html")


class TestPollAnswerView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_employee.profile.company = self.user_owner.profile.company
        self.user_employee.profile.save()
        self.questionnaire = QuestionnaireFactory.create(
            company=self.user_owner.profile.company, type=Questionnaire.Type.POLL
        )
        self.question = QuestionFactory.create(questionnaire=self.questionnaire)
        self.answers = AnswerFactory.create_batch(5, question=self.question)
        self.poll = PollFactory.create(questionnaire=self.questionnaire)
        self.test_answer_data = {"csrfmiddlewaretoken": "xxx", "Favourite colour?": "3", "Favourite dish?": "5"}

    def test_if_poll_answer_is_created(self):
        self.client.force_login(self.user_employee)
        response = self.client.post(reverse("poll-answer", kwargs={"pk": 1}), data=self.test_answer_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(PollAnswer.objects.count(), 1)

    def test_if_message_is_shown_if_poll_answer_was_created(self):
        self.client.force_login(self.user_employee)
        response = self.client.post(reverse("poll-answer", kwargs={"pk": 1}), data=self.test_answer_data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.message, "Your answer was successfully saved.")


class TestPollCloseView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner1 = OwnerFactory.create()
        self.user_owner2 = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_employee.profile.company = self.user_owner1.profile.company
        self.user_employee.profile.save()
        self.user_candidate = CandidateFactory.create()
        self.questionnaire = QuestionnaireFactory.create(
            company=self.user_owner1.profile.company, type=Questionnaire.Type.POLL
        )
        self.question = QuestionFactory.create(questionnaire=self.questionnaire)
        self.answers = AnswerFactory.create_batch(5, question=self.question)
        self.poll = PollFactory.create(questionnaire=self.questionnaire)
        test_answer_data = {"csrfmiddlewaretoken": "xxx", self.question.text: "3"}
        results = json.dumps(test_answer_data)
        for number in range(0, 10):
            user_employee = EmployeeFactory.create()
            user_employee.profile.company = self.user_owner1.profile.company
            PollAnswer.objects.create(
                respondent=user_employee, date_filled="2030-10-10", poll=self.poll, result=results
            )

    @tag("x")
    def test_if_poll_is_successfully_closed(self):
        self.client.force_login(self.user_owner1)
        response = self.client.post(reverse("poll-close", kwargs={"pk": 1}), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PollResults.objects.count(), 1)
        self.poll.refresh_from_db()
        self.assertFalse(self.poll.status)

    def test_if_poll_results_are_created_after_closing_poll(self):
        self.client.force_login(self.user_owner1)
        response = self.client.post(reverse("poll-close", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(PollResults.objects.count(), 1)

    def test_if_regular_employee_cant_close_poll(self):
        self.client.force_login(self.user_employee)
        response = self.client.post(reverse("poll-close", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(PollResults.objects.count(), 0)


class TestPollListView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner1 = OwnerFactory.create()
        self.user_owner2 = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_employee.profile.company = self.user_owner1.profile.company
        self.user_employee.profile.save()
        self.user_candidate = CandidateFactory.create()
        self.questionnaire = QuestionnaireFactory.create(
            company=self.user_owner1.profile.company, type=Questionnaire.Type.POLL
        )
        self.question = QuestionFactory.create(questionnaire=self.questionnaire)
        self.answers = AnswerFactory.create_batch(5, question=self.question)
        self.poll1 = PollFactory.create(questionnaire=self.questionnaire)
        self.poll2 = PollFactory.create(questionnaire=self.questionnaire)

    def test_if_owner_can_access_list_of_polls(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("poll-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context["polls"]), 2)

    def test_if_owner_cant_see_other_company_polls(self):
        self.client.force_login(self.user_owner2)
        response = self.client.get(reverse("poll-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context["polls"]), 0)

    def test_if_candidate_cant_access_view_and_is_redirected_to_correct_dashboard(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("poll-list"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("dashboard-candidate"))

    def test_if_regular_employee_cant_access_view_and_is_redirected_to_correct_dashboard(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("poll-list"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("dashboard-employee"))

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("poll-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "polls/poll_list.html")


class TestPollResultsView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner1 = OwnerFactory.create()
        self.user_owner2 = OwnerFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_employee.profile.company = self.user_owner1.profile.company
        self.user_employee.profile.save()
        self.user_candidate = CandidateFactory.create()
        self.questionnaire = QuestionnaireFactory.create(
            company=self.user_owner1.profile.company, type=Questionnaire.Type.POLL
        )
        self.question = QuestionFactory.create(questionnaire=self.questionnaire)
        self.answers = AnswerFactory.create_batch(5, question=self.question)
        self.poll = PollFactory.create(questionnaire=self.questionnaire)
        test_answer_data = {"csrfmiddlewaretoken": "xxx", self.question.text: "3"}
        results = json.dumps(test_answer_data)
        for number in range(0, 10):
            user_employee = EmployeeFactory.create()
            user_employee.profile.company = self.user_owner1.profile.company
            PollAnswer.objects.create(
                respondent=user_employee, date_filled="2030-10-10", poll=self.poll, result=results
            )
        self.client.force_login(self.user_owner1)
        self.client.post(reverse("poll-close", kwargs={"pk": 1}))
        self.client.logout()

    def test_if_owner_can_access_view(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("poll-results", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_regular_employee_can_access_view(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("poll-results", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_candidate_cant_access_view(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("poll-results", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_owner_cant_access_view_if_another_company_results_and_is_redirected(self):
        self.client.force_login(self.user_owner2)
        response = self.client.get(reverse("poll-results", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_owner_cant_access_view_if_another_company_is_redirected(self):
        self.client.force_login(self.user_owner2)
        response = self.client.get(reverse("poll-results", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_most_picked_answer_is_correct(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("poll-results", kwargs={"pk": 1}))
        self.assertEqual(response.context["most_picked"][0].id, 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_answers_are_correctly_counted(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("poll-results", kwargs={"pk": 1}))
        self.assertEqual(response.context["display_results"].get(self.question).get(self.answers[2]), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("poll-results", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "polls/poll_results.html")
