from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from recruitment.models import Company


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
