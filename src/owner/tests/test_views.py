from django.contrib.auth.models import Group
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status

from users.factories import EmployeeFactory, OwnerFactory


class TestPollCreateView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_manager = EmployeeFactory.create()
        manager_group = Group.objects.get(name="Manager")
        manager_group.user_set.add(self.user_manager)

    def test_if_owner_can_access_view(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("department-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_if_manager_cant_access_view_and_is_redirected_to_correct_dashboard(self):
    #     self.client.force_login(self.user_manager)
    #     response = self.client.get(reverse("poll-create"))
    #     self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    #     self.assertRedirects(response, reverse("dashboard-candidate"))
