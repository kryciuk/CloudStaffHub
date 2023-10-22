from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

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

    @property
    def days_till(self):
        days_till = self.event_date - now()
        days_till_stripped = str(days_till).split(",")[0]
        if days_till_stripped[0] == "-":
            days_till_stripped = days_till_stripped[1:]
        return days_till_stripped

    @property
    def is_past(self):
        return self.event_date < now()


class Event(models.Model):
    name = models.CharField(max_length=120)
    event_date = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
