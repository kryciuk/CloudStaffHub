from django.contrib import admin

from polls.models import Poll, PollAnswer

admin.site.register(Poll)
admin.site.register(PollAnswer)