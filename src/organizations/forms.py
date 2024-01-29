from django import forms

from organizations.models import Company, CompanyProfile, Industry


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        error_messages = {
            "domain_incorrect": "The specified domain is not a valid email domain.",
            "domain_missing": "Company domain is required.",
            "domain_taken": "Company with this domain already exists.",
            "company_name_taken": "Company with this name already exists.",
            "company_name_missing": "Company name is required.",
        }

    def clean_name(self):
        if self.cleaned_data["name"]:
            name = self.cleaned_data["name"]
            if Company.objects.filter(name=name).exists():
                raise forms.ValidationError(self.Meta.error_messages["company_name_taken"], code="company_name_taken")
            return name
        raise forms.ValidationError(self.Meta.error_messages["company_name_missing"], code="company_name_missing")

    def clean_email_domain(self):
        if self.cleaned_data["email_domain"]:
            email_domain = self.cleaned_data["email_domain"]
            if Company.objects.filter(email_domain=email_domain).exists():
                raise forms.ValidationError(self.Meta.error_messages["domain_taken"], code="domain_taken")
            elif "." not in email_domain:
                raise forms.ValidationError(self.Meta.error_messages["domain_incorrect"], code="domain_incorrect")
            return email_domain.lower()
        raise forms.ValidationError(self.Meta.error_messages["domain_missing"], code="domain_missing")


class CompanyProfileForm(forms.ModelForm):
    industries = forms.ModelMultipleChoiceField(queryset=Industry.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = CompanyProfile
        fields = ["industries", "info", "company_logo"]
        help_texts = {"info": None}
