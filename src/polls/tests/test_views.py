# from django.test import tag
# from django.test import TransactionTestCase
# from django.urls import reverse
# from rest_framework import status
#
# from users.factories import CandidateFactory, OwnerFactory, EmployeeFactory
#
#
# class TestPollAnswerView(TransactionTestCase):
#     reset_sequences = True
#
#     def setUp(self):
#         self.user_owner = OwnerFactory.create()
#         self.user_employee = EmployeeFactory.create()
#         self.user_candidate = CandidateFactory.create()
#
#     def test_if_candidate_cant_access_view(self):
#         self.client.force_login(self.user_candidate)
#         response = self.client.get(reverse("city-create"))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_if_regular_employee_cant_access_view(self):
#         self.client.force_login(self.user_employee)
#         response = self.client.get(reverse("city-create"))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_if_owner_can_access_view(self):
#         self.client.force_login(self.user_owner)
#         response = self.client.get(reverse("city-create"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_correct_template_is_used(self):
#         self.client.force_login(self.user_owner)
#         response = self.client.get(reverse("city-create"))
#         self.assertTemplateUsed(response, "recruiter/city_create.html")
