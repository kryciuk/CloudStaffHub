from django import forms

from organizations.models import Company, CompanyProfile, Industry


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"

    def clean_email_domain(self):
        email_domain = self.cleaned_data["email_domain"]
        return email_domain.lower()


class CompanyProfileForm(forms.ModelForm):
    industries = forms.ModelMultipleChoiceField(queryset=Industry.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = CompanyProfile
        fields = ["industries", "info"]
        help_texts = {"info": None}
