from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User

from recruitment.models import Company
from users.models import Profile


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


class UserProfileForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'group']
