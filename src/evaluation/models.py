from django.contrib.auth.models import User
from django.db import models


class Questionnaire(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


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
    questionare = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, related_name="questions"
    )

    def __str__(self):
        return f"{self.text}"


class Evaluation(models.Model):
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="employee"
    )
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manager")
    date = models.DateField()
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
