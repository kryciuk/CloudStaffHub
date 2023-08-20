from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse


class Position(models.Model):
    class Departament(models.TextChoices):
        BOARD_OF_DIRECTORS = 'Board of Directors'
        MARKETING = 'Marketing'
        SALES = 'Sales'
        PROJECT = 'Project'
        DESIGN = 'Design'
        PRODUCTION = 'Production'
        MAINTENANCE = 'Maintenance'
        STORE = 'Store'
        PROCUREMENT = 'Procurement'
        QUALITY = 'Quality'
        INSPECTION = 'Inspection'
        PACKAGING = 'Packaging'
        FINANCE = 'Finance'
        ACCOUNTING = 'Accounting'
        INFORMATION_TECHNOLOGY = 'Information Technology'
        RESEARCH_DEVELOPMENT = 'Research Development'
        HUMAN_RESOURCE = 'Human Resource'
        SECURITY = 'Security'
        ADMINISTRATION = 'Administration'

    class Level(models.TextChoices):
        ENTRY = "Entry"
        JUNIOR = "Junior"
        MID = "Mid"
        SENIOR = "Senior"
        MANAGER = "Manager"

    title = models.CharField(max_length=100, help_text="title of the position")
    level = models.TextField(choices=Level.choices)
    departament = models.TextField(choices=Departament.choices)

    class Meta:
        unique_together = ["title", "level", "departament"]

    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"

    def get_absolute_url(self):
        return reverse("recruiter-default")

    def department_name(self):
        return self.Departament(self.departament).label


class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("recruiter-default")


class Company(models.Model):
    name = models.CharField(max_length=50)
    email_domain = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
