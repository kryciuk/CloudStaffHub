from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse


class Position(models.Model):
    class Departament(models.IntegerChoices):
        BOARD_OF_DIRECTORS = 0
        MARKETING = 1
        SALES = 2
        PROJECT = 3
        DESIGN = 4
        PRODUCTION = 5
        MAINTENANCE = 6
        STORE = 7
        PROCUREMENT = 8
        QUALITY = 9
        INSPECTION = 10
        PACKAGING = 11
        FINANCE = 12
        ACCOUNTING = 13
        INFORMATION_TECHNOLOGY = 14
        RESEARCH_DEVELOPMENT = 15
        HUMAN_RESOURCE = 16
        SECURITY = 17
        ADMINISTRATION = 18

    class Level(models.IntegerChoices):
        ENTRY = 0
        JUNIOR = 1
        MID = 2
        SENIOR = 3
        MANAGER = 4

    title = models.CharField(max_length=100, help_text="title of the position")
    level = models.IntegerField(choices=Level.choices)
    departament = models.IntegerField(choices=Departament.choices)

    class Meta:
        unique_together = ["title", "level", "departament"]

    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"

    def get_absolute_url(self):
        return reverse("recruiter-default")


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
