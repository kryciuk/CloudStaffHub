from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse

from organizations.models import Company


class Questionnaire(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.id}"


class Answer(models.Model):
    answer = models.CharField(max_length=200)
    score = models.IntegerField()
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="answers"
    )

    def __str__(self):
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
    date = models.DateField()
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
