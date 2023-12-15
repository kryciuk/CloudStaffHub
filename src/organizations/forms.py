from django import forms

from organizations.models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"

    def clean_email_domain(self):
        email_domain = self.cleaned_data["email_domain"]
        return email_domain.lower()