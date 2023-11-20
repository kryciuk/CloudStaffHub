from django.contrib.auth.models import Group, User
from django.db import models
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField

from organizations.models import Company, Department, Industry, Position
from recruitment.models import Company


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=True, blank=True)
    interested_in = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="media/users/profile_pic", default="media/users/profile_pic/default.jpg")

    def __str__(self):
        return f"{self.user} profile"

    def get_absolute_url(self):
        return reverse("company-admin")
