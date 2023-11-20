from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

from users.factories import OwnerFactory, EmployeeFactory, CandidateFactory
from core.base import has_group


class TestLoginView(TestCase):
    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()

    def test_login_denied_wrong_password(self):
        login_wrong_password = self.client.login(username=self.user_candidate.username, password="wrong_password")
        self.assertFalse(login_wrong_password)

    def test_login_success_right_password(self):
        login_right_password = self.client.login(username=self.user_candidate.username, password="password")
        self.assertTrue(login_right_password)

    def test_login_redirects_to_dashboard_after_successful_login(self):
        response_owner = self.client.post(
            reverse("login"), {"username": self.user_owner.username, "password": "password"}
        )
        self.assertRedirects(response_owner, reverse("dashboard-employee"))
        response_candidate = self.client.post(
            reverse("login"), {"username": self.user_candidate.username, "password": "password"}
        )
        self.assertRedirects(response_candidate, reverse("dashboard-candidate"))

    def test_login_redirects_to_dashboard_when_logged_user(self):
        self.client.force_login(self.user_owner)
        response_owner = self.client.get(reverse("login"))
        self.assertRedirects(response_owner, reverse("dashboard-employee"))

    def test_correct_template_is_used(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "users/authorization/login.html")

    def test_message_are_shown_after_successful_or_unsuccessful_login(self):
        response_successful_login = self.client.post(
            reverse("login"), {"username": self.user_owner.username, "password": "password"}, follow=True
        )
        message = list(response_successful_login.context.get("messages"))[0]
        self.assertEqual(message.tags, "success")
        self.assertEqual(message.message, "Logged in successfully. Welcome to CloudStaffHub.")
        response_unsuccessful_login = self.client.post(
            reverse("login"), {"username": self.user_owner.username, "password": "wrong_password"}, follow=True
        )
        message = list(response_unsuccessful_login.context.get("messages"))[0]
        self.assertEqual(message.tags, "warning")
        self.assertEqual(message.message, "Your login details are incorrect.")


class TestLogoutView(TestCase):
    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()

    def test_if_logges_out_user(self):
        self.client.force_login(self.user_owner)
        response_logout = self.client.post(reverse("logout"))
        request = response_logout.wsgi_request
        self.assertEqual(request.user.is_authenticated, False)

    def test_correct_template_is_used(self):
        response = self.client.get(reverse("logout"))
        self.assertTemplateUsed(response, "users/authorization/logout.html")


class TestRegisterView(TestCase):
    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.user_employee = EmployeeFactory.create()
        self.data = {"username": "testuser", "first_name": "John",
                     "last_name": "Smith", "email": f"testuser@{self.user_owner.profile.company.email_domain}",
                     "password1": "Miksery1!", "password2": "Miksery1!"}

    def test_if_registers_candidate_correctly(self):
        self.data['email'] = 'testuser@example.com'
        self.client.post(reverse("register"), data=self.data)
        created_user = User.objects.get(username="testuser")
        self.assertTrue(created_user)
        self.assertTrue(has_group(created_user, "Candidate"))

    def test_if_registers_employee_correctly(self):
        self.client.post(reverse("register"), data=self.data)
        created_user = User.objects.get(username="testuser")
        self.assertTrue(created_user)
        self.assertTrue(has_group(created_user, "Employee"))

    def test_if_registration_fails_if_incorrect_data(self):
        self.data["email"] = ""
        self.client.post(reverse("register"), data=self.data)
        created_user = User.objects.filter(username="testuser").first()
        self.assertFalse(created_user)

    def test_message_is_shown_after_successful_registration(self):
        response = self.client.post(reverse("register"), data=self.data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "success")
        self.assertEqual(message.message, f"Account created successfully for {self.data.get('username')}.")

    def test_message_is_shown_after_unsuccessful_registration(self):
        self.data["email"] = ""
        response = self.client.post(reverse("register"), data=self.data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "warning")
        self.assertEqual(message.message['email'][0], f"Email is required.")

    def test_correct_template_is_used(self):
        response = self.client.get(reverse("register"))
        self.assertTemplateUsed(response, "users/authorization/register.html")


class TestPasswordResetView(TestCase):
    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()

    def test_email_is_sent_if_email_in_database(self):
        response = self.client.post(reverse('password_reset'), data={'email': self.user_owner.email})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Password Reset on CloudStaffHub")

    def test_email_is_not_sent_if_email_is_not_in_database(self):
        response = self.client.post(reverse('password_reset'), data={'email': 'test_user2@test.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "warning")
        self.assertEqual(message.message['email'][0], "There is no user registered with the specified email address!")

    def test_correct_template_is_used(self):
        response = self.client.get(reverse("password_reset"))
        self.assertTemplateUsed(response, "users/password_reset/password_reset.html")


class TestPasswordResetDoneView(TestCase):

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()

    def test_correct_template_is_used(self):
        session = self.client.session
        session.update({"previous_view": "UserPasswordResetView"})
        session.save()
        response = self.client.get(reverse("password_reset_done"))
        self.assertTemplateUsed(response, "users/password_reset/password_reset_done.html")


class TestPasswordResetCompleteView(TestCase):

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()

    def test_correct_template_is_used(self):
        session = self.client.session
        session.update({"previous_view": "PasswordResetConfirmView"})
        session.save()
        response = self.client.get(reverse("password_reset_complete"))
        self.assertTemplateUsed(response, "users/password_reset/password_reset_complete.html")


class TestProfileEditByOwnerView(TestCase):

    def setUp(self):
        self.user_owner = OwnerFactory.create()
        self.user_candidate = CandidateFactory.create()
        self.data = {"first_name": "Joan", "last_name": "Smith"}

    def test_only_owner_can_access_view(self):
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse("profile-edit", kwargs={"pk": self.user_candidate.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        self.client.force_login(self.user_candidate)
        response = self.client.get(reverse("profile-edit", kwargs={"pk": self.user_candidate.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
