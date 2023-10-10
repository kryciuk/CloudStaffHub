from django.contrib.auth.models import User
from django.db import models

from organizations.models import Company


class Assignment(models.Model):
    name = models.CharField(max_length=120)
    event_date = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    employee = models.ManyToManyField(User, related_name="employee_assignment")
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manager_assignment", null=True, blank=True)
    status = models.BooleanField(help_text="mark as complete", default=False)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=120)
    event_date = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
