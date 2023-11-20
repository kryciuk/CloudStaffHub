from django import forms
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from users.forms import CreateUserForm, UserInfoEditByOwnerForm, PasswordResetFormCustom, UserProfileUpdateForm
from organizations.models import Industry


class TestCreateUserForm(TestCase):

    def setUp(self):
        self.form_data = {"username": "BossABC",
                          "first_name": "Test",
                          "last_name": "User",
                          "email": "testuser@gmail.com",
                          "password1": "Miksery1!",
                          "password2": "Miksery1!"}

    def test_if_user_is_registered_if_correct_data(self):
        form = CreateUserForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_user_is_not_registered_if_missing_data(self):
        self.form_data.pop("first_name")
        form = CreateUserForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_if_user_is_not_registered_if_passwords_dont_match(self):
        self.form_data["password2"] = "Miksery2!"
        form = CreateUserForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)


class TestUserInfoEditByOwnerForm(TestCase):

    def setUp(self):
        self.group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
        self.form_data = {"first_name": "Test",
                          "last_name": "User",
                          "email": "testuser@gmail.com",
                          "group": self.group.queryset[1]
                          }

    def test_if_user_data_is_changed(self):
        form = UserInfoEditByOwnerForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_if_user_data_is_not_changed_if_incorrect_data(self):
        self.form_data["email"] = ""
        form = UserInfoEditByOwnerForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class TestUserProfileUpdateForm(TestCase):

    def setUp(self):
        self.interested_in = Industry.objects.get(industry=Industry.IndustryChoice.ACCOUNTING)
        self.form_data = {"phone_number": "503440576",
                          "interested_in": self.interested_in}

    def test_if_valid_if_correct_data(self):
        form = UserProfileUpdateForm(data=self.form_data)
        self.assertTrue(form.is_valid())


# class TestAdminEditFormSet(TestCase):
#
#     def setUp(self):
#         self.group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
#         self.company = Company.objects.create(name="ABC", email_domain="abc.com")
#         self.department = Department.objects.create(name=Department.DepartmentChoices.ACCOUNTING, company=self.company)
#         self.form_data = {"first_name": "Test",
#                           "last_name": "User",
#                           "email": "testuser@abc.com",
#                           "group": self.group.queryset[1],
#                           "departament": self.department
#                           }
#
#     def test_if_user_data_is_changed(self):
#         form = AdminEditFormSet(data=self.form_data)
#         print(form)
#         self.assertTrue(form.is_valid())


class TestPasswordResetFormCustom(TestCase):

    def setUp(self):
        self.form_data = {"email": "testuser@gmail.com"}
        self.data = {"username": "testuser", "first_name": "John",
                     "last_name": "Smith", "email": f"testuser@gmail.com",
                     "password1": "Miksery1!", "password2": "Miksery1!"}

    def test_if_error_if_no_email_in_database(self):
        form = PasswordResetFormCustom(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_if_valid_if_email_in_database(self):
        self.client.post(reverse("register"), data=self.data)
        form = PasswordResetFormCustom(data=self.form_data)
        self.assertTrue(form.is_valid())
