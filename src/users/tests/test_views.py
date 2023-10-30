from django.test import TestCase
from django.urls import reverse

from .setup_for_tests import setUp_for_tests


class TestLoginView(TestCase):
    def setUp(self):
        self.user_owner, self.user_candidate = setUp_for_tests()

    def test_login_denied_wrong_password(self):
        login_wrong_password = self.client.login(username=self.user_candidate.username, password="wrong_password")
        self.assertFalse(login_wrong_password)

    def test_login_success_right_password(self):
        login_right_password = self.client.login(username=self.user_candidate.username, password="password")
        self.assertTrue(login_right_password)

    def test_login_redirects_to_dashboard_after_successful_login(self):
        response_owner = self.client.post(reverse("login"),
                                          {"username": self.user_owner.username, "password": "password"})
        self.assertRedirects(response_owner, reverse('dashboard-employee'))
        response_candidate = self.client.post(reverse("login"),
                                              {"username": self.user_candidate.username, "password": "password"})
        self.assertRedirects(response_candidate, reverse('dashboard-candidate'))

    def test_correct_template_is_used(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "users/authorization/login.html")

    def test_message_are_shown_after_successful_or_unsuccessful_login(self):
        response_successful_login = self.client.post(reverse("login"),
                                                     {"username": self.user_owner.username, "password": "password"},
                                                     follow=True)
        message = list(response_successful_login.context.get('messages'))[0]
        self.assertEqual(message.tags, 'success')
        self.assertEqual(message.message, "Logged in successfully. Welcome to CloudStaffHub.")
        response_unsuccessful_login = self.client.post(reverse("login"),
                                                       {"username": self.user_owner.username,
                                                        "password": "wrong_password"}, follow=True)
        message = list(response_unsuccessful_login.context.get('messages'))[0]
        self.assertEqual(message.tags, 'warning')
        self.assertEqual(message.message, "Your login details are incorrect.")


class TestLogoutView(TestCase):
    def setUp(self):
        self.user_owner, self.user_candidate = setUp_for_tests()

    # def test_logout_(self):
    #     response_owner = self.client.post(reverse("logout"), follow=True)
    #     self.assertRedirects(response_owner, reverse('login'))