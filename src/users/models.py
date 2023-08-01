from django import forms
from django.contrib.auth.models import Group, User
from django.db import models
from django.shortcuts import reverse

from recruitment.models import Company


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user} profile"
