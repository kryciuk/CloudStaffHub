from django.contrib import admin

from events.models import Assignment, Event

admin.site.register(Assignment)
admin.site.register(Event)

__all__ = ["admin"]
