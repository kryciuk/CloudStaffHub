from django.db import models
from django.contrib.auth.models import User
from evaluation.choices import ANSWERS_CHOICES


class Question(models.Model):
    prompt = models.TextField()


class Response(models.Model):
    response_opt = models.IntegerField(choices=ANSWERS_CHOICES, default=3)


class Questionnaire(models.Model):
    question = models.ManyToManyField(Question)


class Evaluation(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee")
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manager")
    date = models.DateField()
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
