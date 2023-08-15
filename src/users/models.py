from django.contrib.auth.models import Group, User
from django.db import models
from django.shortcuts import reverse

from recruitment.models import Company
from organizations.models import Position


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(null=True, blank=True)
    interested_in = models.IntegerField(choices=Position.Departament.choices)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user} profile"

    def get_absolute_url(self):
        return reverse("company-admin")
