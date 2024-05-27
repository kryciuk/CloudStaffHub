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
    status = models.BooleanField(default=True, help_text="will this questionnaire be ever used again")
    type = models.TextField(choices=Type.choices)

    def __str__(self) -> str:
        return f"{self.name}"


class Answer(models.Model):
    answer = models.CharField(max_length=200)
    score = models.IntegerField(null=True, blank=True)
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="answers")

    def __str__(self) -> str:
        if self.score is None:
            return f"{self.answer}"

        return f"{self.answer} ({self.score})"

    def __repr__(self) -> str:
        if self.score is None:
            return f"{self.answer}"

        return f"{self.answer} ({self.score})"


class Question(models.Model):
    text = models.CharField(max_length=200)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="questions")

    def __str__(self) -> str:
        return f"{self.text}"

    def get_absolute_url(self):
        reverse("dashboard-manager")


class Evaluation(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee")
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manager")
    date_created = models.DateField()
    date_end = models.DateTimeField()
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    result_employee = models.JSONField("", null=True, blank=True)
    result_manager = models.JSONField("", null=True, blank=True)
    status_employee = models.BooleanField(default=False, help_text="true if evaluation filled by the employee")
    status_manager = models.BooleanField(default=False, help_text="true if evaluation filled by the manager")

    def __str__(self) -> str:
        return f"{self.questionnaire} for {self.employee.first_name} {self.employee.last_name}"

    def get_absolute_url(self):
        reverse("dashboard-manager")
