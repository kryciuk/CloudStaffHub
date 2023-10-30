from django.contrib import admin

from organizations.models import (City, Company, CompanyProfile, Industry,
                                  Position, Department)

admin.site.register(Position)
admin.site.register(Company)
admin.site.register(City)
admin.site.register(CompanyProfile)
admin.site.register(Industry)
admin.site.register(Department)
