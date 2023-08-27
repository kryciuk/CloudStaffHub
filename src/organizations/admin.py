from django.contrib import admin

from recruitment.models import City, Company, Position

admin.site.register(Position)
admin.site.register(Company)
admin.site.register(City)
