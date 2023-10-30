from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.forms import inlineformset_factory

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


class UserInfoEditByOwnerForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "group", ]
        labels = {"first_name": "First Name",
                  "last_name": "Last Name",
                  "email": "Email",
                  "group": "Group"}


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number", "interested_in", "profile_pic"]
        labels = {"phone_number": "Phone Number",
                  "interested_in": "Interests",
                  "profile_pic": "Profile Picture"}


AdminEditFormSet = inlineformset_factory(
    User, Profile, fields=('department',),
    extra=1, can_delete=False, can_delete_extra=False)
