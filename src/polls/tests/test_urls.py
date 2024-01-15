from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status

from evaluation.factories import QuestionnaireFactory
from polls.factories import PollFactory
from polls.models import PollAnswer, PollResults
from users.factories import CandidateFactory, EmployeeFactory, OwnerFactory


class TestUrls(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_candidate = CandidateFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.user_owner = OwnerFactory.create()
        self.questionnaire = QuestionnaireFactory.create(company=self.user_owner.profile.company)
        self.poll = PollFactory.create(questionnaire=self.questionnaire, status=True)
        self.poll_answer = PollAnswer(
            respondent=self.user_employee, date_filled="2030-01-01", poll=self.poll, result={}
        )
        self.poll_answer.save()
        self.poll_results = PollResults(poll=self.poll, results={}, close_date="2030-10-10")
        self.poll_results.save()
        self.urls = {
            "poll-create": reverse("poll-create"),
            "poll-list": reverse("poll-list"),
            "poll-fill": reverse("poll-fill", kwargs={"pk": 1}),
            "poll-results": reverse("poll-results", kwargs={"pk": 1}),
        }

    def test_polls_urls_are_callable_by_name_for_owner(self):
        self.client.force_login(self.user_owner)
        for name, url in self.urls.items():
            with self.subTest(url_name=name):
                res = self.client.get(url)
                self.assertEqual(res.status_code, status.HTTP_200_OK)
