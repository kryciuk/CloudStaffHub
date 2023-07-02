from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .choices import (
    POSITION_DEPARTMENT_CHOICES,
    JOB_APPLICATION_STATUS_CHOICES,
    JOB_OFFER_LEVEL_CHOICES,
    JOB_OFFER_CITIES_CHOICES,
)


class Position(models.Model):
    title = models.CharField(max_length=100, help_text="title of the position")
    description = models.TextField(help_text="description of the position")
    departament = models.IntegerField(choices=POSITION_DEPARTMENT_CHOICES, default=0)

    def __str__(self):
        return self.title


class JobOffer(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.BooleanField(help_text="is job offer active?")
    city = models.IntegerField(choices=JOB_OFFER_CITIES_CHOICES, default=0)
    level = models.IntegerField(choices=JOB_OFFER_LEVEL_CHOICES, default=0)
    published_date = models.DateField()
    expiry_date = models.DateField()

    def __str__(self):
        return f"{self.position} (ID: {self.id})"

    def get_absolute_url(self):
        return reverse("job_offer_detail", args=[str(self.id)])


class JobApplication(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    job_offer = models.ForeignKey(
        JobOffer, on_delete=models.CASCADE, help_text="reply to job offer"
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, default="test")
    phone_number = models.IntegerField(help_text="cellular number")
    email = models.EmailField()
    expected_salary = models.IntegerField(help_text="expected gross salary")
    cv = models.FileField(
        upload_to="recrutitment/media/cv", default="bla.pdf", blank=True
    )  # recruitment
    # certificates = models.ImageField(upload_to='pdf')
    consent_processing_data = models.BooleanField(
        help_text="consent to processing of personal data"
    )
    status = models.IntegerField(
        choices=JOB_APPLICATION_STATUS_CHOICES, default=0, blank=True
    )

    def get_absolute_url(self):
        return reverse("job_offer_detail", args=[str(self.job_offer.id)])
