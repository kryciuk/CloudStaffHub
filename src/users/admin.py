from django.contrib import admin

from .models import Profile

admin.site.register(Profile)

__all__ = ["admin"]
