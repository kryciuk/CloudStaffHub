from django.db import models
from django.shortcuts import reverse


class Position(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100, default="Finance")

    def __str__(self):
        return self.title


class JobOffer(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.BooleanField()
    date_start = models.DateField()
    date_stop = models.DateField()

    def get_absolute_url(self):
        return reverse('job_offer_detail', args=[str(self.id)])
