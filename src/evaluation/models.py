from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse

from organizations.models import Company


class Questionnaire(models.Model):
    class Type(models.TextChoices):
        EVALUATION = "Evaluation"
        POLL = "Poll"

    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(
        default=True, help_text="will this questionnaire be ever used again"
    )
    type = models.TextField(choices=Type.choices)

    def __str__(self):
        return f"{self.name} ID:{self.id}"


class Answer(models.Model):
    answer = models.CharField(max_length=200)
    score = models.IntegerField()
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="answers"
    )
    picked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.answer} ({self.score})"

    def __repr__(self):
        return f"{self.answer} ({self.score})"


class Question(models.Model):
    text = models.CharField(max_length=200)
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, related_name="questions"
    )

    def __str__(self):
        return f"{self.text}"

    def get_absolute_url(self):
        reverse("dashboard-manager")


class Evaluation(models.Model):
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="employee"
    )
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manager")
    date_created = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    result = models.JSONField("", null=True, blank=True)
    status = models.BooleanField(
        default=False, help_text="true if evaluation filled by an employee"
    )

    def __str__(self):
        return f"{self.questionnaire}"

    def get_absolute_url(self):
        reverse("dashboard-manager")
