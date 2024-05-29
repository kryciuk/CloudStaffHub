from django.shortcuts import reverse
from django.test import TransactionTestCase
from rest_framework import status

from evaluation.factories import (
    AnswerFactory,
    EvaluationFactory,
    QuestionFactory,
    QuestionnaireFactory,
)
from evaluation.models import Answer, Question, Questionnaire
from users.factories import CandidateFactory, EmployeeFactory, OwnerFactory


class TestQuestionnaireCreateView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner1 = OwnerFactory()
        self.user_employee = EmployeeFactory()
        self.user_employee.profile.company = self.user_owner1.profile.company
        self.user_employee.profile.save()
        self.form_data = {"name": "Performance evaluation", "type": Questionnaire.Type.EVALUATION}
        self.user_candidate = CandidateFactory()

    def test_owner_can_access_questionnaire_create(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("questionnaire-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_employee_cant_access_questionnaire_create(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("questionnaire-create"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_owner_can_create_questionnaire(self):
        self.client.force_login(self.user_owner1)
        response = self.client.post(reverse("questionnaire-create"), data=self.form_data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Questionnaire.objects.count(), 1)

    def test_if_title_is_correct(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("questionnaire-create"))
        title = response.context["title"]
        self.assertEqual(title, "Create Questionnaire - CloudStaffHub")

    def test_if_correct_template_used(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("questionnaire-create"))
        self.assertTemplateUsed(response, "evaluation/questionnaire/questionnaire_create.html")

    def test_if_message_is_shown_if_access_is_denied(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("questionnaire-create"), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.message, "You don't have the required permissions to access this page.")


class TestQuestionnaireDetailView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner1 = OwnerFactory()
        self.user_employee = EmployeeFactory()
        self.user_employee.profile.company = self.user_owner1.profile.company
        self.user_employee.profile.save()
        self.questionnaire = QuestionnaireFactory.create(
            company=self.user_owner1.profile.company, created_by=self.user_owner1
        )
        self.question = QuestionFactory.create(questionnaire=self.questionnaire)
        self.answers = AnswerFactory.create_batch(5, question=self.question)

    def test_owner_can_access_questionnaire_detail(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("questionnaire-detail", kwargs={"pk": self.questionnaire.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_employee_cant_access_questionnaire_detail(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("questionnaire-detail", kwargs={"pk": self.questionnaire.id}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_owner_can_view_details_of_questionnaire(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("questionnaire-detail", kwargs={"pk": self.questionnaire.id}))
        self.assertEqual(response.context["questionnaire"], self.questionnaire)
        self.assertEqual(
            list(response.context["questions"]), list(Question.objects.filter(questionnaire=self.questionnaire))
        )
        self.assertEqual(
            list(response.context["answers"][self.question]), list(Answer.objects.filter(question=self.question))
        )

    def test_if_correct_template_used(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("questionnaire-detail", kwargs={"pk": self.questionnaire.id}))
        self.assertTemplateUsed(response, "evaluation/questionnaire/questionnaire_detail.html")

    def test_if_message_is_shown_if_access_is_denied(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("questionnaire-detail", kwargs={"pk": self.questionnaire.id}), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.message, "You don't have the required permissions to access this page.")

    def test_if_title_is_correct(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("questionnaire-detail", kwargs={"pk": self.questionnaire.id}), follow=True)
        title = response.context["title"]
        self.assertEqual(title, "Questionnaire Details - CloudStaffHub")

    # @tag("y")
    # def test_if_owner_can_close_questionnaire(self):
    #     self.client.force_login(self.user_owner1)
    #     response = self.client.post(reverse("questionnaire-close", kwargs={"pk": self.questionnaire.id}))
    #     self.questionnaire.refresh_from_db()
    #     self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    #     self.assertFalse(self.questionnaire.status)


class TestEvaluationDetailView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner1 = OwnerFactory()
        self.user_employee1 = EmployeeFactory()
        self.user_employee2 = EmployeeFactory()
        self.user_employee1.profile.company = self.user_owner1.profile.company
        self.user_employee1.profile.save()
        self.user_employee2.profile.company = self.user_owner1.profile.company
        self.user_employee2.profile.save()
        self.questionnaire = QuestionnaireFactory.create(
            company=self.user_owner1.profile.company, created_by=self.user_owner1
        )
        self.question = QuestionFactory.create(questionnaire=self.questionnaire)
        self.answers = AnswerFactory.create_batch(5, question=self.question)
        self.evaluation = EvaluationFactory.create(
            manager=self.user_owner1, employee=self.user_employee1, questionnaire=self.questionnaire
        )
        self.user_candidate = CandidateFactory.create()

    def test_owner_can_access_evaluation_detail(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("evaluation-detail", kwargs={"pk": self.evaluation.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_assigned_employee_can_access_evaluation_detail(self):
        self.client.force_login(self.user_employee1)
        response = self.client.get(reverse("evaluation-detail", kwargs={"pk": self.evaluation.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_candidate_cant_access_evaluation_detail(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("evaluation-detail", kwargs={"pk": self.evaluation.id}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_not_assigned_employee_cant_access_evaluation_detail(self):
        self.client.force_login(self.user_employee2)
        response = self.client.get(reverse("evaluation-detail", kwargs={"pk": self.evaluation.id}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_correct_template_used(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("evaluation-detail", kwargs={"pk": self.evaluation.id}))
        self.assertTemplateUsed(response, "evaluation/evaluation/evaluation_detail.html")

    def test_if_message_is_shown_if_access_is_denied(self):
        self.client.force_login(self.user_employee2)
        response = self.client.get(reverse("evaluation-detail", kwargs={"pk": self.evaluation.id}), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.message, "You don't have the required permissions to access this page.")

    def test_if_title_is_correct(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("evaluation-detail", kwargs={"pk": self.evaluation.id}))
        title = response.context["title"]
        self.assertEqual(title, f"Evaluation ID:{self.evaluation.id} - CloudStaffHub")


class TestQuestionnaireFillView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner1 = OwnerFactory()
        self.user_employee1 = EmployeeFactory()
        self.user_employee2 = EmployeeFactory()
        self.user_employee1.profile.company = self.user_owner1.profile.company
        self.user_employee1.profile.save()
        self.user_employee2.profile.company = self.user_owner1.profile.company
        self.user_employee2.profile.save()
        self.questionnaire = QuestionnaireFactory.create(
            company=self.user_owner1.profile.company, created_by=self.user_owner1
        )
        self.question = QuestionFactory.create(questionnaire=self.questionnaire)
        self.answers = AnswerFactory.create_batch(5, question=self.question)
        self.evaluation = EvaluationFactory.create(
            manager=self.user_owner1, employee=self.user_employee1, questionnaire=self.questionnaire
        )
        self.user_candidate = CandidateFactory.create()

    def test_owner_can_access_questionnaire_fill(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(
            reverse("questionnaire-fill", kwargs={"id_evaluation": self.evaluation.id, "pk": self.questionnaire.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_assigned_employee_can_access_questionnaire_fill(self):
        self.client.force_login(self.user_employee1)
        response = self.client.get(
            reverse("questionnaire-fill", kwargs={"id_evaluation": self.evaluation.id, "pk": self.questionnaire.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_candidate_cant_access_questionnaire_fill(self):
        self.client.force_login(self.user_candidate)
        response = self.client.get(
            reverse("questionnaire-fill", kwargs={"id_evaluation": self.evaluation.id, "pk": self.questionnaire.id})
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_correct_template_used(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(
            reverse("questionnaire-fill", kwargs={"id_evaluation": self.evaluation.id, "pk": self.questionnaire.id})
        )
        self.assertTemplateUsed(response, "evaluation/questionnaire/questionnaire_fill.html")

    def test_if_message_is_shown_if_access_is_denied(self):
        self.client.force_login(self.user_employee2)
        response = self.client.get(
            reverse("questionnaire-fill", kwargs={"id_evaluation": self.evaluation.id, "pk": self.questionnaire.id}),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.message, "You don't have the required permissions to access this page.")

    def test_if_title_is_correct(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(
            reverse("questionnaire-fill", kwargs={"id_evaluation": self.evaluation.id, "pk": self.questionnaire.id})
        )
        title = response.context["title"]
        self.assertEqual(title, f"Evaluation Fill ID:{self.evaluation.id} - CloudStaffHub")
