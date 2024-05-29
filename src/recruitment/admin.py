from django.contrib import admin

from recruitment.models import JobApplication, JobOffer

admin.site.register(JobOffer)
admin.site.register(JobApplication)

__all__ = ["admin"]
