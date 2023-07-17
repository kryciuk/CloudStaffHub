from django.contrib import admin

from recruitment.models import Company, JobApplication, JobOffer, Position

admin.site.register(Position)
admin.site.register(JobOffer)
admin.site.register(JobApplication)
admin.site.register(Company)
