from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
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
        labels = {
            "username": "Username",
            "first_name": "First name",
            "last_name": "Last name",
            "email": "Email",
        }

        error_messages = {
            'username_exists': "User with this username already exists!",
            'email_exists': "User with this email already exists!",
            'password_mismatch': "The two password fields didn't match.",
            'first_name_required': "First name is required.",
            'last_name_required': "Last name is required.",
            'email_required': "Email is required.",
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.Meta.error_messages['username_exists'], code='username_exists')
        return username

    def clean_first_name(self):
        if self.cleaned_data["first_name"]:
            return self.cleaned_data["first_name"].capitalize()
        raise forms.ValidationError(self.Meta.error_messages['first_name_required'], code='first_name_required')

    def clean_last_name(self):
        if self.cleaned_data["last_name"]:
            return self.cleaned_data["last_name"].capitalize()
        raise forms.ValidationError(self.Meta.error_messages['last_name_required'], code='last_name_required')

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(self.Meta.error_messages['email_exists'], code='email_exists')
            return email.lower()
        raise forms.ValidationError(self.Meta.error_messages['email_required'], code='email_required')


class UserInfoEditByOwnerForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "group",
        ]
        labels = {"first_name": "First Name", "last_name": "Last Name", "email": "Email", "group": "Group"}
        error_messages = {
            'email_required': "Email is required.",
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            raise forms.ValidationError(self.Meta.error_messages['email_required'], code='email_required')
        return email.lower()


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number", "interested_in", "profile_pic"]
        labels = {"phone_number": "Phone Number", "interested_in": "Interests", "profile_pic": "Profile Picture"}


AdminEditFormSet = inlineformset_factory(
    User, Profile, fields=("department",), extra=1, can_delete=False, can_delete_extra=False
)


class PasswordResetFormCustom(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with the specified email address!")
        return email
