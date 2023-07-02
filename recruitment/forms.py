from django.forms import ModelForm
from .models import JobApplication, JobOffer


class JobOfferForm(ModelForm):
    class Meta:
        model = JobOffer
        fields = "__all__"
        labels = {"status": "Is this job offer active?"}
        help_texts = {
            "position": None,
            "description": None,
            "status": None,
            "city": None,
            "published_date": None,
            "expiry_date": None,
        }


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
            "expected_salary": "Expected  gross salary",
            "cv": "CV",
            "consent_processing_data": "I hereby give consent for my personal data to be processed by ["
            "nazwa firmy] for the purpose of conducting recruitment for the "
            "position for which I am applying.",
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
