import pytz
from django.forms import ChoiceField, ModelForm, forms
from django.utils import timezone

from organizations.models import City

from .models import JobApplication, JobOffer


class JobOfferForm(ModelForm):
    country = ChoiceField(choices=[])

    class Meta:
        model = JobOffer
        fields = "__all__"
        exclude = ["company", "published_date", "status"]
        help_texts = {
            "position": None,
            "description": None,
            "city": None,
            "published_date": None,
            "expiry_date": None,
        }
        error_messages = {"expiry_date_future": "The expiry date must be in the future."}

    def __init__(self, *args, **kwargs):
        super(JobOfferForm, self).__init__(*args, **kwargs)

        countries_with_cities = City.objects.values_list("country", flat=True).distinct()

        country_choices = [(country_code, City.Country(country_code).label) for country_code in countries_with_cities]

        self.fields["country"].choices = country_choices

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data["expiry_date"]
        tz = pytz.timezone("Europe/Warsaw")
        today = timezone.datetime.today()
        today = today.astimezone(tz)
        if expiry_date < today:
            raise forms.ValidationError(self.Meta.error_messages["expiry_date_future"], code="expiry_date_future")
        return expiry_date


class JobOfferFormUpdate(ModelForm):
    class Meta:
        model = JobOffer
        fields = "__all__"
        exclude = ["company", "published_date"]
        labels = {"status": "Is this job offer open?"}
        help_texts = {
            "position": None,
            "description": None,
            "city": None,
            "published_date": None,
            "expiry_date": None,
            "status": None,
        }
        error_messages = {"expiry_date_future": "The expiry date must be in the future."}

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data["expiry_date"]
        tz = pytz.timezone("UTC")
        today = timezone.datetime.today()
        today = today.astimezone(tz)
        if expiry_date < today:
            raise forms.ValidationError(self.Meta.error_messages["expiry_date_future"], code="expiry_date_future")
        return expiry_date


class JobApplicationForm(ModelForm):
    class Meta:
        model = JobApplication
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "expected_salary",
            "cv",
            "consent_processing_data",
        )
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "phone_number": "Phone Number",
            "email": "Email",
            "expected_salary": "Expected Gross Salary",
            "cv": "CV",
            "consent_processing_data": "I hereby give consent for my personal data to be processed for the purpose of "
            "conducting recruitment for the position for which I am applying.",
        }
        help_texts = {
            "first_name": None,
            "last_name": None,
            "phone_number": None,
            "email": None,
            "expected_salary": None,
            "cv": None,
            "consent_processing_data": None,
        }
        error_messages = {
            "consent_processing_data_required": "Consent to processing data is required.",
            "cv_required": "CV is required.",
        }

    def clean_consent_processing_data(self):
        consent_processing_data = self.cleaned_data["consent_processing_data"]
        if consent_processing_data is not True:
            raise forms.ValidationError(
                self.Meta.error_messages["consent_processing_data_required"], code="consent_processing_data_required"
            )
        return consent_processing_data

    def clean_cv(self):
        cv = self.cleaned_data["cv"]
        if cv is None:
            raise forms.ValidationError(self.Meta.error_messages["cv_required"], code="cv_required")
        return cv


class JobApplicationStatusForm(ModelForm):
    class Meta:
        model = JobApplication
        fields = ["status"]
