from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse

from organizations.models import Company
from evaluation.models import Questionnaire, Question, Answer


class Poll(models.Model):
    date_end = models.DateField()
    date_created = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    status = models.BooleanField(default=True, help_text="true if poll open")

    def __str__(self):
        return f"Poll: {self.questionnaire}"

    def get_absolute_url(self):
        reverse("dashboard-manager")


class PollAnswer(models.Model):
    respondent = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="respondent"
    )
    date_filled = models.DateField(null=True, blank=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="related_poll")
    result = models.JSONField("", null=True, blank=True)

    class Meta:
        unique_together = ["respondent", "poll"]

    def __str__(self):
        return f"{self.respondent} answer to: {self.poll.questionnaire}"

    def get_absolute_url(self):
        reverse("dashboard-manager")