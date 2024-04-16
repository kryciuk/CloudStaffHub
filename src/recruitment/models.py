from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField

from organizations.models import City, Company, Position


class JobOffer(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    description = models.TextField(help_text="description of the position")
    status = models.BooleanField(help_text="is job offer active?")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    published_date = models.DateField()
    expiry_date = models.DateTimeField()

    def __str__(self):
        return f"{self.position} (ID: {self.id})"

    def get_absolute_url(self):
        return reverse("job-offer-detail", args=[str(self.id)])


class JobApplication(models.Model):
    class Status(models.IntegerChoices):
        RECEIVED = 0
        UNDER_REVIEW = 1
        CLOSED = 2
        APPROVED = 3

    candidate = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, help_text="reply to job offer")
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = PhoneNumberField(help_text="cellular number")
    email = models.EmailField()
    expected_salary = models.IntegerField(help_text="expected gross salary")
    cv = models.FileField(upload_to="recruitment/media/cv")
    consent_processing_data = models.BooleanField(help_text="consent to processing of personal data")
    status = models.IntegerField(choices=Status.choices, default=0, blank=True)

    def get_absolute_url(self):
        return reverse("job-offers")

    def __str__(self):
        return f"ID:{self.id} {self.candidate.first_name} {self.candidate.last_name}"
